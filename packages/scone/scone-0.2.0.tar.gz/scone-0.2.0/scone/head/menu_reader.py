#  Copyright 2020, Olivier 'reivilibre'.
#
#  This file is part of Scone.
#
#  Scone is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Scone is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Scone.  If not, see <https://www.gnu.org/licenses/>.

import logging
import os
import typing
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Deque, Dict, Iterable, List, Optional, Set, Tuple, Union

import attr
import textx

from scone.head.dag import RecipeDag, Resource
from scone.head.recipe import RecipeContext
from scone.head.variables import Variables

if typing.TYPE_CHECKING:
    from scone.head.head import Head
    from scone.head.recipe import Recipe


def _load_grammar():
    grammar_file_path = Path(Path(__file__).parent, "grammar", "scoml.tx")
    return textx.metamodel_from_file(grammar_file_path)


scoml_grammar = _load_grammar()
scoml_classes = scoml_grammar.namespaces["scoml"]

logger = logging.getLogger(__name__)


class ControlDirective:
    def iter_over(self, vars: Variables) -> Iterable[Variables]:
        raise NotImplementedError("Abstract.")


@attr.s(auto_attribs=True)
class ForDirective(ControlDirective):
    """
    For loop_variable in collection
    """

    # The name of the variable that should be taken on by the iteration
    loop_variable: str

    # List of literals or str for a variable (by name)
    collection: Union[str, List[Any]]

    def iter_over(self, vars: Variables):
        to_iter = self.collection
        if isinstance(to_iter, str):
            to_iter = vars.get_dotted(to_iter)

        if not isinstance(to_iter, list):
            raise ValueError(f"to_iter = {to_iter!r} not a list")

        for item in to_iter:
            new_vars = Variables(vars)
            new_vars.set_dotted(self.loop_variable, item)
            yield new_vars


@attr.s(auto_attribs=True)
class IfDirective(ControlDirective):
    def condition_true(self, vars: Variables) -> bool:
        return False

    def iter_over(self, vars: Variables) -> Iterable[Variables]:
        if self.condition_true(vars):
            yield vars
        else:
            yield from ()


@attr.s(auto_attribs=True)
class IfSetDirective(IfDirective):
    # Name of the variable to check for existence.
    check_variable: str

    def condition_true(self, vars: Variables) -> bool:
        return vars.has_dotted(self.check_variable)


@attr.s(auto_attribs=True)
class IfCondDirective(IfDirective):
    # Name of the variable
    variable: str

    # The operator that is used
    operator: str

    # The other value to check for equality against
    other_value: str

    def condition_true(self, vars: Variables) -> bool:
        if self.operator == "=":
            value = vars.get_dotted(self.variable)
            return value == self.other_value
        else:
            raise NotImplementedError(f"operator {self.operator} not understood.")


@attr.s(auto_attribs=True)
class RecipeEdgeDirective:
    # "after" or "before"
    kind: str

    recipe_id: str


@attr.s(auto_attribs=True)
class ResourceEdgeDirective:
    # "needs", "wants" or "provides"
    kind: str

    resource: Resource


@attr.s(auto_attribs=True)
class ListenEdgeDirective:
    # "when" or "only when"
    kind: str

    recipe_or_resource: Union[str, Resource]


@attr.s(auto_attribs=True, eq=False)
class MenuBlock:
    id: Optional[None]

    human: str

    contents: List[Union["MenuBlock", "MenuRecipe"]]

    parent: Optional["MenuBlock"]

    user_directive: Optional[str] = None
    sous_directive: Optional[str] = None
    control_directives: List[ControlDirective] = attr.ib(factory=list)
    import_directives: List[str] = attr.ib(factory=list)
    recipe_edges: List[RecipeEdgeDirective] = attr.ib(factory=list)
    resource_edges: List[ResourceEdgeDirective] = attr.ib(factory=list)


@attr.s(auto_attribs=True, eq=False)
class MenuRecipe:
    kind: str

    id: Optional[str]

    human: str

    arguments: Dict[str, Any]

    parent: MenuBlock

    user_directive: Optional[str] = None
    sous_directive: Optional[str] = None
    control_directives: List[ControlDirective] = attr.ib(factory=list)
    recipe_edges: List[RecipeEdgeDirective] = attr.ib(factory=list)
    resource_edges: List[ResourceEdgeDirective] = attr.ib(factory=list)
    listen_edges: List[ListenEdgeDirective] = attr.ib(factory=list)


def convert_textx_value(txvalue) -> Union[list, str, int, bool, dict]:
    if isinstance(txvalue, scoml_classes["NaturalList"]):
        return [convert_textx_value(element) for element in txvalue.elements]
    elif (
        isinstance(txvalue, scoml_classes["QuotedString"])
        or isinstance(txvalue, scoml_classes["UnquotedString"])
        or isinstance(txvalue, scoml_classes["Integer"])
        or isinstance(txvalue, scoml_classes["Boolean"])
    ):
        return txvalue.value
    elif isinstance(txvalue, scoml_classes["BracketList"]):
        return [convert_textx_value(item) for item in txvalue.items]
    elif isinstance(txvalue, scoml_classes["BraceDict"]):
        result = dict()
        for pair in txvalue.pairs:
            result[convert_textx_value(pair.key)] = convert_textx_value(pair.value)
        return result
    else:
        raise ValueError(f"Unknown SCOML value: {txvalue}")


def convert_textx_recipe(txrecipe_or_subblock, parent: Optional[MenuBlock]):
    if isinstance(txrecipe_or_subblock, scoml_classes["SubBlock"]):
        txsubblock = txrecipe_or_subblock
        menu_block = convert_textx_block(txsubblock.block, parent)
        menu_block.id = txsubblock.unique_id
        menu_block.human = txsubblock.human.strip()

        return menu_block
    elif isinstance(txrecipe_or_subblock, scoml_classes["Recipe"]):
        assert parent is not None
        txrecipe = txrecipe_or_subblock
        args = dict()

        for arg in txrecipe.args:
            args[arg.name] = convert_textx_value(arg.value)
        recipe = MenuRecipe(
            txrecipe.kind, txrecipe.unique_id, txrecipe.human.strip(), args, parent
        )

        for directive in txrecipe.directives:
            if isinstance(directive, scoml_classes["UserDirective"]):
                recipe.user_directive = directive.user
            elif isinstance(directive, scoml_classes["SousDirective"]):
                recipe.sous_directive = directive.sous
            elif isinstance(directive, scoml_classes["ResourceEdgeDirective"]):
                recipe.resource_edges.append(
                    ResourceEdgeDirective(
                        directive.kind[1:], convert_textx_resource(directive.resource)
                    )
                )
            elif isinstance(directive, scoml_classes["RecipeEdgeDirective"]):
                recipe.recipe_edges.append(
                    RecipeEdgeDirective(directive.kind[1:], directive.id)
                )
            elif isinstance(directive, scoml_classes["ListenEdgeDirective"]):
                recipe.listen_edges.append(
                    ListenEdgeDirective(
                        directive.kind[1:],
                        directive.recipe_id
                        or convert_textx_resource(directive.resource),
                    )
                )
            elif isinstance(directive, scoml_classes["ForDirective"]):
                for_list = directive.collection or convert_textx_value(directive.list)
                assert isinstance(for_list, list) or isinstance(for_list, str)
                recipe.control_directives.append(
                    ForDirective(directive.loop_variable, for_list)
                )
            elif isinstance(directive, scoml_classes["IfSetDirective"]):
                var = directive.variable
                assert isinstance(var, str)
                recipe.control_directives.append(IfSetDirective(var))
            elif isinstance(directive, scoml_classes["IfCondDirective"]):
                var = directive.variable
                op = directive.operator
                other_value = convert_textx_value(directive.other_value)
                assert isinstance(var, str)
                assert isinstance(op, str)
                recipe.control_directives.append(IfCondDirective(var, op, other_value))
            else:
                raise ValueError(f"Unknown directive {directive}")

        return recipe
    else:
        raise ValueError("Neither Recipe nor SubBlock: " + str(txrecipe_or_subblock))


def convert_textx_resource(txresource) -> Resource:
    extra_params = None
    if txresource.extra_params is not None:
        extra_params = convert_textx_value(txresource.extra_params)

    sous: Optional[str] = "(self)"  # XXX docstring to warn about this
    if txresource.sous:
        if txresource.sous == "head":
            sous = None
        else:
            sous = txresource.sous

    resource_id = convert_textx_value(txresource.primary)
    assert isinstance(resource_id, str)
    return Resource(txresource.type, resource_id, sous, extra_params)


def convert_textx_block(txblock, parent: Optional[MenuBlock]) -> MenuBlock:
    recipes: List[Union[MenuRecipe, MenuBlock]] = []
    block = MenuBlock(None, "", recipes, parent)

    for recipe in txblock.recipes:
        recipes.append(convert_textx_recipe(recipe, block))

    for directive in txblock.directives:
        if isinstance(directive, scoml_classes["UserDirective"]):
            # TODO(expectation): error if multiple user directives
            block.user_directive = directive.user
        elif isinstance(directive, scoml_classes["SousDirective"]):
            block.sous_directive = directive.sous
        elif isinstance(directive, scoml_classes["ForDirective"]):
            for_list = directive.collection or convert_textx_value(directive.list)
            assert isinstance(for_list, list) or isinstance(for_list, str)
            block.control_directives.append(
                ForDirective(directive.loop_variable, for_list)
            )
        elif isinstance(directive, scoml_classes["IfSetDirective"]):
            var = directive.variable
            assert isinstance(var, str)
            block.control_directives.append(IfSetDirective(var))
        elif isinstance(directive, scoml_classes["IfCondDirective"]):
            var = directive.variable
            op = directive.operator
            other_value = convert_textx_value(directive.other_value)
            assert isinstance(var, str)
            assert isinstance(op, str)
            block.control_directives.append(IfCondDirective(var, op, other_value))
        elif isinstance(directive, scoml_classes["ImportDirective"]):
            block.import_directives.append(directive.importee)
        elif isinstance(directive, scoml_classes["ResourceEdgeDirective"]):
            block.resource_edges.append(
                ResourceEdgeDirective(
                    directive.kind, convert_textx_resource(directive.resource)
                )
            )
        elif isinstance(directive, scoml_classes["RecipeEdgeDirective"]):
            block.recipe_edges.append(RecipeEdgeDirective(directive.kind, directive.id))
        else:
            raise ValueError(f"Unknown directive {directive}")

    return block


SousName = str
ForLoopIndices = Tuple[int, ...]
SingleRecipeInvocationKey = Tuple[SousName, ForLoopIndices]


class MenuLoader:
    def __init__(self, menu_dir: Path, head: "Head"):
        self._menu_dir: Path = menu_dir
        self._units: Dict[str, MenuBlock] = dict()
        self._recipes: Dict[
            MenuRecipe, Dict[SingleRecipeInvocationKey, Recipe]
        ] = defaultdict(dict)
        self._dag: RecipeDag = head.dag
        self._head = head

    @staticmethod
    def _load_menu_unit(full_path: Path, relative: str) -> MenuBlock:
        model = scoml_grammar.model_from_file(full_path)
        return convert_textx_block(model, None)

    def load(self, unit_name: str):
        if unit_name in self._units:
            return

        full_path = Path(self._menu_dir, unit_name + ".scoml")
        menu_block = self._load_menu_unit(full_path, unit_name)
        self._units[unit_name] = menu_block
        for unit in menu_block.import_directives:
            self.load(unit)

    def resolve_ref(
        self, referrer: Union[MenuBlock, MenuRecipe], reference: str
    ) -> Optional[Union[MenuBlock, MenuRecipe]]:
        """
        Resolves a recipe or block reference
        :param referrer: recipe or block making the reference that needs to be resolved
        :param reference: string reference that needs to be resolved
        :return: If found, the menu block or recipe that was referenced.
        """
        # TODO(feature): need to think about scoping rules and then figure
        #  this one out

        # TEMPORARY, UNSTABLE TODO(stabilise) resolution rules
        #   need to consider resolution between files, and IDless resolution

        # get the root ancestor of the referrer
        a: Union[MenuBlock, MenuRecipe] = referrer
        while a.parent is not None:
            a = a.parent

        to_visit: Deque[Union[MenuBlock, MenuRecipe]] = deque()
        to_visit.append(a)

        while to_visit:
            next_node = to_visit.popleft()

            if next_node.id == reference:
                return next_node

            if isinstance(next_node, MenuBlock):
                for child in next_node.contents:
                    to_visit.append(child)

        return None

    def _get_first_common_ancestor(
        self, one: Union[MenuBlock, MenuRecipe], other: Union[MenuBlock, MenuRecipe]
    ) -> Optional[MenuBlock]:
        ancestors_of_a = set()

        a: Optional[Union[MenuBlock, MenuRecipe]] = one
        b: Optional[Union[MenuBlock, MenuRecipe]] = other

        while a:
            ancestors_of_a.add(a)
            a = a.parent

        while b:
            if b in ancestors_of_a:
                assert isinstance(b, MenuBlock)
                return b
            b = b.parent

        return None

    def get_related_instances(
        self,
        sous: str,
        referrer_indices: Tuple[int, ...],
        referrer: Union[MenuBlock, MenuRecipe],
        menu_recipe: MenuRecipe,
    ) -> List["Recipe"]:
        result = []

        first_common_ancestor = self._get_first_common_ancestor(referrer, menu_recipe)

        a: Union[MenuBlock, MenuRecipe] = referrer
        strip = 0
        while a != first_common_ancestor:
            strip += len(a.control_directives)
            parent = a.parent
            assert parent is not None
            a = parent

        a = menu_recipe
        extra = 0
        while a != first_common_ancestor:
            extra += len(a.control_directives)
            parent = a.parent
            assert parent is not None
            a = parent

        for (instance_sous, indices), recipe in self._recipes[menu_recipe].items():
            if sous != instance_sous:
                continue
            if len(referrer_indices) - strip + extra == len(indices):
                if referrer_indices[:-strip] == indices[:-extra]:
                    result.append(recipe)
            else:
                logger.warning(
                    "Mismatch in indices length %r - %d + %d ~/~ %r",
                    referrer_indices,
                    strip,
                    extra,
                    indices,
                )

        return result

    def get_all_menublock_recipes(self, block: MenuBlock) -> Iterable[MenuRecipe]:
        for child in block.contents:
            if isinstance(child, MenuRecipe):
                yield child
            elif isinstance(child, MenuBlock):
                yield from self.get_all_menublock_recipes(child)
            else:
                raise RuntimeError(f"Unknown child {child!r}")

    def dagify_recipe(
        self,
        recipe: MenuRecipe,
        hierarchical_source: str,
        fors: Tuple[ForDirective, ...],
        applicable_souss: Iterable[str],
        sous_mask: Optional[Set[str]],
        applicable_user: Optional[str],
    ):
        recipe_class = self._head.recipe_loader.get_class(recipe.kind)
        if recipe_class is None:
            raise ValueError(f"No recipe class found for {recipe.kind!r}")

        fors = fors + tuple(recipe.control_directives)

        if recipe.user_directive:
            applicable_user = recipe.user_directive

        if recipe.sous_directive:
            applicable_souss = self._head.get_souss_for_hostspec(recipe.sous_directive)
            if sous_mask:
                applicable_souss = set(applicable_souss)
                applicable_souss.intersection_update(sous_mask)

        for sous in applicable_souss:
            if not applicable_user:
                applicable_user = self._head.souss[sous]["user"]
                assert applicable_user is not None

            sous_vars = self._head.variables[sous]
            for context_vars, for_indices in self._control_apply(
                fors, sous_vars, tuple()
            ):
                context = RecipeContext(
                    sous=sous,
                    user=context_vars.eval(applicable_user),
                    slug=recipe.id,
                    hierarchical_source=hierarchical_source,  # XXX
                    human=recipe.human,
                    variables=context_vars,
                )
                try:
                    args = context_vars.substitute_in_dict_copy(recipe.arguments)
                except KeyError as ke:
                    raise KeyError(
                        f"When substituting for {hierarchical_source} / {recipe}"
                    ) from ke
                instance: Recipe = recipe_class.new(context, args, self._head)
                self._recipes[recipe][(sous, for_indices)] = instance
                self._dag.add(instance)

    def dagify_block(
        self,
        block: MenuBlock,
        hierarchical_source: str,
        fors: Tuple[ForDirective, ...],
        applicable_souss: Iterable[str],
        sous_mask: Optional[Set[str]],
        applicable_user: Optional[str],
    ):
        fors = fors + tuple(block.control_directives)

        if block.user_directive:
            applicable_user = block.user_directive

        if block.sous_directive:
            applicable_souss = self._head.get_souss_for_hostspec(block.sous_directive)
            if sous_mask:
                applicable_souss = set(applicable_souss)
                applicable_souss.intersection_update(sous_mask)

        for content in block.contents:
            if isinstance(content, MenuBlock):
                block_name = content.id or "?"
                self.dagify_block(
                    content,
                    f"{hierarchical_source}.{block_name}",
                    fors,
                    applicable_souss,
                    sous_mask,
                    applicable_user,
                )
            elif isinstance(content, MenuRecipe):
                self.dagify_recipe(
                    content,
                    hierarchical_source,
                    fors,
                    applicable_souss,
                    sous_mask,
                    applicable_user,
                )
            else:
                raise ValueError(f"{content}?")

    def substitute_vars_in_resource(
        self, vars: Variables, resource: Resource
    ) -> Resource:
        evalled_id = vars.eval(resource.id)
        return attr.evolve(resource, id=evalled_id)

    def postdagify_recipe(
        self,
        recipe: MenuRecipe,
        fors: Tuple[ForDirective, ...],
        applicable_souss: Iterable[str],
        sous_mask: Optional[Set[str]],
    ) -> None:
        # TODO(feature): add edges

        # add fors
        fors = fors + tuple(recipe.control_directives)

        if recipe.sous_directive:
            applicable_souss = self._head.get_souss_for_hostspec(recipe.sous_directive)
            if sous_mask:
                applicable_souss = set(applicable_souss)
                applicable_souss.intersection_update(sous_mask)

        for sous in applicable_souss:
            sous_vars = self._head.variables[sous]
            for context_vars, for_indices in self._control_apply(
                fors, sous_vars, tuple()
            ):
                instance = self._recipes[recipe][(sous, for_indices)]  # noqa

                for recipe_edge in recipe.recipe_edges:
                    target = self.resolve_ref(recipe, recipe_edge.recipe_id)

                    if isinstance(target, MenuBlock):
                        # Get all recipes and apply the edge to them.
                        for target_recipe in self.get_all_menublock_recipes(target):
                            for target_instance in self.get_related_instances(
                                sous, for_indices, recipe, target_recipe
                            ):
                                if recipe_edge.kind == "after":
                                    self._dag.add_ordering(target_instance, instance)
                                elif recipe_edge.kind == "before":
                                    self._dag.add_ordering(instance, target_instance)
                    elif isinstance(target, MenuRecipe):
                        for target_instance in self.get_related_instances(
                            sous, for_indices, recipe, target
                        ):
                            if recipe_edge.kind == "after":
                                self._dag.add_ordering(target_instance, instance)
                            elif recipe_edge.kind == "before":
                                self._dag.add_ordering(instance, target_instance)

                for resource_edge in recipe.resource_edges:
                    resource = self.substitute_vars_in_resource(
                        context_vars, resource_edge.resource
                    )

                    if resource.sous == "(self)":
                        resource = attr.evolve(resource, sous=sous)

                    if resource_edge.kind == "needs":
                        self._dag.needs(instance, resource)
                    elif resource_edge.kind == "wants":
                        self._dag.needs(instance, resource, soft_wants=True)
                    elif resource_edge.kind == "provides":
                        self._dag.provides(instance, resource)

                for listen_edge in recipe.listen_edges:
                    if isinstance(listen_edge.recipe_or_resource, Resource):
                        # TODO(design): is it right for this to NEED it rather
                        #   than WANT it?
                        resource = listen_edge.recipe_or_resource
                        if resource.sous == "(self)":
                            resource = attr.evolve(resource, sous=sous)
                        self._dag.needs(instance, resource)
                        self._dag.watches(
                            instance,
                            resource,
                            listen_edge.kind == "only when",
                        )
                    elif isinstance(listen_edge.recipe_or_resource, str):
                        target = self.resolve_ref(
                            recipe, listen_edge.recipe_or_resource
                        )

                        if isinstance(target, MenuRecipe):
                            for target_instance in self.get_related_instances(
                                sous, for_indices, recipe, target
                            ):
                                self._dag.add_ordering(target_instance, instance)
                                self._dag.watches(
                                    instance,
                                    target_instance,
                                    listen_edge.kind == "only when",
                                )
                        else:
                            raise RuntimeError(f"not supported on target: {target!r}")

                # XXX apply edges from parent

    def postdagify_block(
        self,
        block: MenuBlock,
        fors: Tuple[ForDirective, ...],
        applicable_souss: Iterable[str],
        sous_mask: Optional[Set[str]],
    ):
        # XXX pass down specific edges here

        # TODO(feature): add edges

        fors = fors + tuple(block.control_directives)

        if block.sous_directive:
            applicable_souss = self._head.get_souss_for_hostspec(block.sous_directive)
            if sous_mask:
                applicable_souss = set(applicable_souss)
                applicable_souss.intersection_update(sous_mask)

        for content in block.contents:
            if isinstance(content, MenuBlock):
                self.postdagify_block(content, fors, applicable_souss, sous_mask)
            elif isinstance(content, MenuRecipe):
                self.postdagify_recipe(content, fors, applicable_souss, sous_mask)
            else:
                raise ValueError(f"{content}?")

    def dagify_all(self, sous_subset: Optional[Set[str]]):
        for name, unit in self._units.items():
            self.dagify_block(
                unit,
                name,
                tuple(),
                self._head.get_souss_for_hostspec("all"),
                sous_subset,
                None,
            )
        for _name, unit in self._units.items():
            self.postdagify_block(
                unit, tuple(), self._head.get_souss_for_hostspec("all"), sous_subset
            )

    def _control_apply(
        self,
        controls: Tuple[ControlDirective, ...],
        vars: "Variables",
        accum: Tuple[int, ...],
    ) -> Iterable[Tuple["Variables", Tuple[int, ...]]]:
        if not controls:
            yield vars, accum
            return

        head = controls[0]
        tail = controls[1:]

        for idx, new_vars in enumerate(head.iter_over(vars)):
            yield from self._control_apply(tail, new_vars, accum + (idx,))

    def load_menus_in_dir(self) -> RecipeDag:
        dag = RecipeDag()

        for root, dirs, files in os.walk(self._menu_dir):
            for file in files:
                if not file.endswith(".scoml"):
                    continue
                # full_path = Path(root, file)
                # load this as a menu file
                pieces = file.split(".")
                assert len(pieces) == 2
                self.load(pieces[0])

        return dag
