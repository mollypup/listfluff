from atproto import Client
import httpx


def resolve_pds(did):
    if did.startswith("did:plc:"):
        r = httpx.get(f"https://plc.directory/{did}")
        r.raise_for_status()
    elif did.startswith("did:web"):
        r = httpx.get(f"https://{did.lstrip("did:web")}/.well-known/did.json")
        r.raise_for_status()
    else:
        raise ValueError("Invalid DID Method")
    for service in r.json()["service"]:
        if service["id"] == "#atproto_pds":
            return service["serviceEndpoint"]


def resolve_handle(user):
    if user.startswith("did:"):
        did = user
    else:
        pub = Client("https://public.api.bsky.app")
        did = pub.resolve_handle(user).did

    return did


def create_client(user, password):
    did = resolve_handle(user)
    client = Client(resolve_pds(did))
    client.login(did, password)
    return client


def get_followers(did):
    cursor = None
    dids = []
    pub = Client("https://public.api.bsky.app")
    while True:
        response = pub.com.atproto.server.get_followers(
            params=models.com.atproto.server.get_followers.Params(
                did=did,
                limit=100,
                cursor=cursor,
            )
        )

        cursor = response.cursor

        dids_i = [f.did for f in response.followers]
        dids.extend(dids_i)

        if not cursor:
            break
    return dids


def split_list(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]
