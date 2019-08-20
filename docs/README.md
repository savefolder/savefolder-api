# SaveFolderAPI Docs
This is SaveFolderAPI - general purpose API for each and every SaveFolder service.

## Service connection workflow

1. Each service must have a `service token` - an entity, which identifies service in api.
With every request to api service must pass its `service token`. 
For HTTP requests, `service token` is passed in `Service-Token` request header.
`Service token` (for now) is obtained directly from SavefolderAPI development team.
Under all circumstances, service must keep its `service token` in secret.

2. On request from a user, service first must get a `user token` - an entity, which identifies user in api.
With every request, which interacts with user data, service must pass corresponding `user token`.
For HTTP requests, `user token` is passed in `User-Token` request header.
As `user token` is a user identifier, you should keep it secure, as all personal data.
But without `service token` `user token` is essentially just an identifier, as it is impossible to gain
access to any user-related data by using only `user token`.
    - to get user token use `/account/token` API method.
   
3. There are three ways to upload image to SaveFolderAPI.
    1. URL
    2. Base64 encoded data
    3. Multipart upload, using `multipart/form-data` content type
    
    From these methods, 3rd is preferred, due to faster request processing.
    Also first two methods pose real security threat, and probably will be removed in future versions.
    So it is advised to use 3rd method.   
    
    - to upload image use `/image/upload` API method

4. To download image from SaveFolderAPI, service must get a download link.
All download links have expiration time, with default value set to 300 seconds, or 5 minutes.
Max download url expiration time equal to 3600 seconds, or 1 hour.
If requested expiration time exceeds this limit, it will be reduced to it.
    - to request image download url use `/image/download_url` API method
    
5. To get, add, assign or delete tags service must use relevant HTTP method. 
    - all interaction with tags is done via `/image/tags` API method
    
6. API provides service-agnostic image search, based on tags.
All service-dependent search customization must be done on relevant service side.
    - to search images based on their tags use `/images/search` API method

7. For users present in multiple services, SaveFolderAPI will provide data synchronization method.
This feature is still in development.
    - to merge two accounts use `/account/merge` API method

## API Specification

For API specification please refer to `api.md` document.
