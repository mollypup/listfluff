from atproto import models

from helpers import resolve_handle, get_followers, split_list


def remove_users_from_list(client, users, list_uri):
    dids = [resolve_handle(user) for user in users]
    dids = list(set(dids))
    remove_dids_from_list(client, dids, list_uri)


def remove_followers_from_list(client, users, list_uri):
    udids = [resolve_handle(user) for user in users]
    dids = []
    for udid in udids:
        dids.extend(get_followers(udid))
    dids = list(set(dids))
    remove_dids_from_list(client, dids, list_uri)


def remove_dids_from_list(client, dids, list_uri):
    records = []
    repo = client._session.did
    cursor = None
    while True:
        response = client.com.atproto.repo.list_records(
            params=models.com.atproto.repo.list_records.Params(
                collection="app.bsky.graph.listitem",
                cursor=cursor,
                repo=repo,
                limit=100,
            )
        )

        cursor = response.cursor
        records.extend(response.records)

        if not cursor:
            break

    set_of_dids = set(dids)
    rkeys_to_remove = []
    for record in records:
        if record.value.subject in set_of_dids:
            rkeys_to_remove.append(record.uri.split("/")[-1])

    items = [models.com.atproto.repo.apply_writes.Delete(
        collection="app.bsky.graph.listitem",
        rkey=rkey) for rkey in rkeys_to_remove]

    splitty = split_list(items, 200)
    for s in splitty:
        client.com.atproto.repo.apply_writes(
            data=models.com.atproto.repo.apply_writes.Data(
                repo=repo,
                writes=s
            )
        )
