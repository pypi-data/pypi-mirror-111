from itertools import groupby
from typing import List

from attr import field

from pyinaturalist.constants import JsonResponse
from pyinaturalist.models import Taxon, TaxonCount, TaxonCounts, define_model, kwarg


@define_model
class LifeListTaxon(TaxonCount):
    """A single taxon in a user's life list"""

    descendant_obs_count: int = field(default=0)
    direct_obs_count: int = field(default=0)

    @property
    def indent_level(self) -> int:
        """Indentation level corresponding to this item's rank level"""
        return int(((70 - self.rank_level) / 5))

    def __str__(self) -> str:
        padding = " " * self.indent_level
        return f'[{self.id:<8}] {padding} {self.rank.title()} {self.name}: {self.count}'


@define_model
class LifeList(TaxonCounts):
    """A user's life list, based on the schema of ``GET /observations/taxonomy``"""

    count_without_taxon: int = field(default=0)
    taxa: List[LifeListTaxon] = field(factory=list, converter=LifeListTaxon.from_json_list)  # type: ignore
    user_id: int = kwarg

    @classmethod
    def from_json(cls, value: JsonResponse, user_id: int = None, **kwargs) -> 'LifeListTaxon':  # type: ignore
        count_without_taxon = value.get('count_without_taxon', 0)
        if 'results' in value:
            value = value['results']

        life_list_json = {'taxa': value, 'user_id': user_id, 'count_without_taxon': count_without_taxon}
        return super(LifeList, cls).from_json(life_list_json)  # type: ignore

    def tree(self):
        """**Experimental**
        Organize this life list into a taxonomic tree

        Returns:
            :py:class:`rich.tree.Tree`
        """
        return make_tree(self.taxa)


def make_tree(taxa: List[Taxon]):
    """Organize a list of taxa into a taxonomic tree. Must contain at least one taxon with
    'Life' (taxon ID 48460) as its parent.

    Returns:
        :py:class:`rich.tree.Tree`
    """

    from rich.tree import Tree

    taxa_by_parent_id = _sort_groupby(taxa, key=lambda x: x.parent_id or -1)

    def make_child_tree(node, taxon):
        """Add a taxon and its children to the specified tree node.
        Base case: leaf taxon (with no children)
        Recursive case: non-leaf taxon (with children)
        """
        node = node.add(taxon.full_name)
        for child in taxa_by_parent_id.get(taxon.id, []):
            node.add(make_child_tree(node, child))
        return node

    tree_root = {'id': 48460, 'name': 'Life', 'rank': 'State of matter'}
    return make_child_tree(Tree('life list', expanded=False), Taxon.from_json(tree_root))


def _sort_groupby(values, key):
    """Apply sorting then grouping using the same key"""
    return {k: list(group) for k, group in groupby(sorted(values, key=key), key=key)}
