from atproto import models

from helpers import resolve_handle, get_followers, split_list


def add_users_to_list(client, users, list_uri):
    dids = [resolve_handle(user) for user in users]
    dids = list(set(dids))
    add_dids_to_list(client, dids, list_uri)


def add_followers_to_list(client, users, list_uri):
    udids = [resolve_handle(user) for user in users]
    dids = []
    for udid in udids:
        dids.extend(get_followers(udid))
    dids = list(set(dids))
    add_dids_to_list(client, dids, list_uri)


def add_dids_to_list(client, dids, list_uri):
    created_at = client.get_current_time_iso()
    list_items = [models.AppBskyGraphListitem.Record(
                  created_at=created_at,
                  list=list_uri,
                  subject=did
                  ) for did in dids]

    list_of_writes = [models.com.atproto.repo.apply_writes.Create(
                      collection="app.bsky.graph.listitem",
                      value=list_item) for list_item in list_items]

    splitty = split_list(list_of_writes, 200)
    repo = client._session.did
    for s in splitty:
        client.com.atproto.repo.apply_writes(
            data=models.com.atproto.repo.apply_writes.Data(
                repo=repo,
                writes=s
            )
        )
