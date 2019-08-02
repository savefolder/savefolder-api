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

- One of the following:
    - `file: base64` &ndash; base64-encoded file
    - `file: bytes` &ndash; raw file content
    - `url: url` &ndash; file download url
- `rid: str` &ndash; (optional) remote image id
- `tags: list` &ndash; (optional) array of image tags

**Output:**

- `duplicate: bool` &ndash; whether if user already had this image
- `id: str` &ndash; internal image id
- `rid: str` &ndash; (optional) remote image id
- `tags: list` &ndash; initial + auto-generated image tags
- `url: url` &ndash; image download url

### Method: `tags.update`

**Input:**

- One of the following:
    - `id: str` &ndash; internal image id
    - `rid: str` &ndash; remote image id
- `action: str` &ndash; (optional) update action
- `tags: list` &ndash; array of image tags

Possible actions: `add`, `remove`, `replace` (default)

**Output:**

- `tags: list` &ndash; updated array of image tags

### Method: `images.delete`

**Input:**

- One of the following:
    - `id: str` &ndash; internal image id
    - `rid: str` &ndash; remote image id

### Method: `images.find`

**Input:**

- One of the following:
    - `<nothing>` &ndash; all user images are returned
    - `query: str` &ndash; find images by search text
    - `id: str` &ndash; find image by internal id
    - `rid: str` &ndash; find image by remote id
- `skip: int = 0` &ndash; (optional) pagination offset
- `limit: int = 10` &ndash; (optional) pagination size

**Output (array):**

- `id: str` &ndash; internal image id
- `rid: str` &ndash; (optional) remote image id
- `tags: list` &ndash; image tags
- `url: url` &ndash; image download url

### Method: `account.merge`

**Input:** 

- `key: str` &ndash; (optional) account merge key

If `key` is not provided method generates a new one. \
Otherwise attempts to merge accounts using provided key.

**Output:**

- One of the following, depending on presence of `key`:
    - `token: str` &ndash; api token of merged account
    - `key: str` &ndash; freshly generated merge key

### Method: `tokens.acquire` [service]

**Input:**

- `rid: str` &ndash; user remote id
- `create: bool = true` &ndash; (optional) create account if not existing

**Output:**

- `token: str` &ndash; api token for given `rid`
- `created: bool` &ndash; whether if new account was created
