# Collections

## User collection

- users

### Description
This collection is used to store user data

### Document structure
```json
{
  "_id": "user identifier in api",
  "images": [
    {
      "_id": "image identifier"
    }
  ]
}
```

## Service collections

- vk
- tg
- ds

### Description
These collections are used to store service-related user data 

### Document structure
```json
{
  "_id": "user identifier in api",
  "user_id": "user identifier in service",
  "token": "user token"
}
```

## Merge collection

- merge

### Description
This collection is used to store user merge data

### Document structure
```json
{
  "_id": "user identifier in api",
  "start": "merge start timestamp",
  "duration": "allowed merge duration",
  "key": "merge key"
}
```
