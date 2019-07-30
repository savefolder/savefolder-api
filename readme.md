SaveFolder API v0
=================

### Method: abstract

**Input:**

- `token: str` &ndash; service or user token

**Output:**

- `{result: <data>}` &ndash; request successful
- `{error: {code: 123, message: 'message'}}` &ndash; shit happens

To check whether if request was succcessfull, just do `if 'error' in data`

### Method: `images.upload`

**Input:**

- `file: str` &ndash; base64-encoded file or file url
- `rid: str` &ndash; (optional) remote image id
- `tags: list` &ndash; (optional) array of image tags

**Output:**

- `id: str` &ndash; internal image id
- `rid: str` &ndash; (optional) remote image id
- `tags: list` &ndash; initial & auto-generated image tags
- `url: url` &ndash; image download url

### Method: `images.update`

**Input:**

- `id: str` &ndash; (optional) image id
- `rid: str` &ndash; (optional) image remote id
- `tags: list` &ndash; (optional) array of image tags
- `delete: bool` &ndash; (optional) whether to delete image

**Output:** `true`

### Method: `images.search`

**Input:**

- `query: str` &ndash; (optional) search text
- `id: str` &ndash; (optional) find image by internal id
- `rid: str` &ndash; (optional) find image by remote id

If all fields are omitted all user images are returned

**Output (array):**

- `id: str` &ndash; internal image id
- `rid: str` &ndash; (optional) remote image id
- `tags: list` &ndash; image tags
- `url: url` &ndash; image download url

### Method: `tokens.aquire`

**Input:** `rid: str` &ndash; user remote id

**Output:** `token: str` &ndash; api token for given `rid`
