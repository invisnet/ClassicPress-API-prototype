#!/usr/bin/env python

from dulwich.objectspec import parse_tree
from dulwich.repo import Repo
from json import dumps
import posixpath
import stat

with Repo('../ClassicPress-release') as r:
    hashes = {}

    def list_tree(store, treeid, base):
        for (name, mode, sha) in store[treeid].iteritems():
            if base:
                name = posixpath.join(base, name)
            hashes[name] = sha
            if stat.S_ISDIR(mode):
                list_tree(store, sha, name)

    tree = parse_tree(r, 'HEAD')
    list_tree(r.object_store, tree.id, "")

print dumps(hashes, sort_keys=True, indent=2)

