SaveFolder API v0
=================

### Method: abstract

**Input:**

- `token: str` &ndash; service or user token

**Output:**

- `{status: 2xx, response: <data>}` &ndash; success
- `{status: 4xx, error: 'message'}` &ndash; shit happens

To check whether if request was successful, just do `if 'error' in data` \
Status code is also accessible as HTTP response status 

### Method: `images.upload`

**Input:**

- `url: url` &ndash; file download url
- `rid: str` &ndash; (optional) remote image id
- `tags: str` &ndash; (optional) user-provided image description

**Output:**

- `duplicate: bool` &ndash; whether if user already had this image
- `id: str` &ndash; internal image id
- `rid: str` &ndash; (optional) remote image id
- `tags: list` &ndash; auto-generated image tags
- `url: url` &ndash; image download url


### Method: `images.update`

**Input:**

- One of the following:
    - `id: str` &ndash; internal image id
    - `rid: str` &ndash; remote image id
- `tags: str` &ndash; user-provided description

**Output:**

- `id: str` &ndash; internal image id
- `rid: str` &ndash; (optional) remote image id
- `tags: list` &ndash; updated image tags
- `url: url` &ndash; image download url


### Method: `images.get`

**Input:**

- One of the following:
    - `id: str` &ndash; internal image id
    - `rid: str` &ndash; remote image id
    
**Output:**

- `id: str` &ndash; internal image id
- `rid: str` &ndash; (optional) remote image id
- `tags: list` &ndash; updated image tags
- `url: url` &ndash; image download url


### Method: `images.delete`

**Input:**

- One of the following:
    - `id: str` &ndash; internal image id
    - `rid: str` &ndash; remote image id


### Method: `tokens.acquire` [service]

**Input:**

- `rid: str` &ndash; user remote id
- `create: bool = true` &ndash; (optional) create account if not existing

**Output:**

- `token: str` &ndash; api token for given `rid`
- `created: bool` &ndash; whether if new account was created


### Method: `search`

**Input:**

- One of the following:
    - `<nothing>` &ndash; all user images are returned
    - `query: str` &ndash; find images by search text
- `offset: int = 0` &ndash; (optional) pagination offset
- `limit: int = 10` &ndash; (optional) pagination limit

**Output (array):**

- `id: str` &ndash; internal image id
- `rid: str` &ndash; (optional) remote image id
- `tags: list` &ndash; image tags
- `url: url` &ndash; image download url
