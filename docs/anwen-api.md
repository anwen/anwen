---
title: Anwen API
brand: anwen.in
version: 0.4.0
---

# Anwen API

### All API calls start with

<pre class="base">
http://anwen.in
</pre>

### Path

For this documentation, we will assume every request begins with the above path.

### Format

All calls are returned in **JSON**.

### Status Codes

- **200** Successful GET and PUT.
- **201** Successful POST.
- **202** Successful Provision queued.
- **204** Successful DELETE
- **401** Unauthenticated.
- **409** Unsuccessful POST, PUT, or DELETE (Will return an errors object)



# Account

## GET /users

Expects basic auth to get an existing customer. API will return **200**.

#### example request

    $ curl http://anwen.in/users


## POST /users

Creates new account. Required fields are username, email, password, and password_confirmation. Possible responses include 201 or 409

#### example request

    $ curl http://anwen.in/users \
      -F "email=anwen.in@gmail.com" \
      -F "password=secret"


## GET /users/:id


## PUT /users/:id

Update your account.

#### example request

    $ curl -u anwen:secret http://anwen.in/account -X PUT \
      -F 'phone=42434243'


# Shares

## GET /shares

Returns collection of public Shares. Response will be 200

#### example request

    $ curl -u http://anwen.in/shares

#### response

    [
      {
        "uri": "/shares/37",
        "title": "goog music",
        "content": "eagles 1973..."
      },
      {
        "uri": "/shares/42",
        "title": "time machine",
        "content": "ssh-rsa AAAdFzzx927..."
      },
      ...
    ]


## POST /shares

Adds a new Share. "key" is a required field and "slug" is optional. Possible responses include 201 or 409.

#### example request

    $ curl -u anwen:secret http://anwen.in/shares \
      -F "title=time-memo" -F "content=/home/anwen/time-memo.md"

OR (file upload)

#### example request

    $ curl -u anwen:secret http://anwen.in/shares \
      -F "name=memo" -F "content=@/home/anwen/time-memo.md"

#### response

    {
      "uri": "/shares/42",
      "name": "memo",
      "key": "rem?..."
    }


## GET /shares/:id

Returns single share. Possible responses 200, or 404

#### example request

    $ curl -u anwen:secret http://anwen.in/shares/42

#### response

    {
      "uri": "/shares/42",
      "name": "memo",
      "key": "rem?..."
    }


## PUT /shares/:id

Updates public key record. Possible responses include 200, or 409

#### example request

    $ curl -u anwen:secret http://anwen.in/shares/43 -X PUT \
      -F "name=a better description"

#### response

    {
      "uri": "/shares/43",
      "name": "a better world",
      "key": "play..."
    }


## DELETE /shares/:id

Deletes share. Api will respond with status 204

#### example request

    $ curl -u anwen:secret http://anwen.in/shares/42 -X DELETE

