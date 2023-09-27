# Short description
It's Django Rest Framework API, which allows any user to upload/download images through HTTP requests.
Registration is mainly through admin panel, but can be simply added if needed.
It uses drf-spectacular & swagger.
It uses Docker.
It implements a way to download original/thumbnail/expiration links to an image.
It has 3 base account tiers, with different links possbility.
You can create your own tiers.
You can list your images.
There are a lot of tests implemented.
# Starting setup (Windows 10)
1. Download Docker
2. Install it
3. Run it
4. There might be a need to call "wsl --update" in your terminal
5. Download the Image uploader project
6. Open terminal/CMD
7. Navigate into project root folder

If it is your first time running it then use:
1. Start Docker
2. Open terminal/CMD
3. Navigate into project root folder
4. docker-compose build
5. docker-compose run --rm app sh -c "python manage.py migrate" (There MIGHT be an issue, depending on your setup, that will require to call it once again)
6. docker-compose run --rm app sh -c "python manage.py loaddata fixtures/init.json" (It will load 3 base Tiers and a Superuser)
7. docker-compose-up

If it is your any next time running it then:
1. Start Docker
2. Open terminal/CMD
3. Navigate into project root folder
4. docker-compose-up

Once everything is up go to:
1. http://127.0.0.1:8000/admin
Email: admin@admin.com
Password: Admin@123!

AND 

2. http://127.0.0.1:8000/api/docs/#/

To being able to test API calls you have to provide user's token first to authenticate the user.
Detailed description of it is provided in the Flow Description section.

# Flow description
Once you are here http://127.0.0.1:8000/admin logged as an admin then you should see something like, that

![InitUsers](https://github.com/Iz4bel4/ImageUploader/assets/112544496/f92c0b08-1aeb-433f-8651-1e3cb232474b)

You can create another user here. There are a lot of validations and mandatory fields so pay attention.

![UserCreation](https://github.com/Iz4bel4/ImageUploader/assets/112544496/0dbe3903-4865-4994-8b76-91432ed4bd47)

Then you can go to "Tiers", if everything is set up correctly then you should have 3 base tiers.

![StartingTiers](https://github.com/Iz4bel4/ImageUploader/assets/112544496/7d141a09-f2c6-458f-8e2a-b64603d0d4ec)

Basic one, which gives you only a possibility to download 200px height thumbnail of your images:

![Basic](https://github.com/Iz4bel4/ImageUploader/assets/112544496/9e0696a9-876b-44c0-8bfc-2bd62416abb1)

Premium one, which allows you to download 200px, 400px height thumbnails and an original image:

![Premium](https://github.com/Iz4bel4/ImageUploader/assets/112544496/59bfaa25-23fc-461f-8302-e175fda02a87)

Enterprise one, which allows same things as Premium one, but additionally lets you download an expiring link

![Enterprise](https://github.com/Iz4bel4/ImageUploader/assets/112544496/840ee9d3-98ed-4935-9be8-44c9d228f042)

You can change them as you want. There is additionally an option to crate your own Tiers.

Let's create a custom tier:

![MyTier](https://github.com/Iz4bel4/ImageUploader/assets/112544496/a4f24b9a-405d-41e4-a175-c4e2b13b44db)

You can set any of them in a certain User's data. Let's start with this one:

![UserTierSetToBasic](https://github.com/Iz4bel4/ImageUploader/assets/112544496/ca12e5b1-2d4e-44ce-9308-66a5604ca511)

Go to the token section in Admin and add an token for your user:

![AddingToken](https://github.com/Iz4bel4/ImageUploader/assets/112544496/71d626d0-b85b-4b0b-9bd5-e89c3db7971e)

Copy it!

![CopyThisKey](https://github.com/Iz4bel4/ImageUploader/assets/112544496/02604584-4dc2-4da3-a91c-f8b1c31eec20)

Now go here http://127.0.0.1:8000/api/docs/#/
You should see something like this:

![Swagger](https://github.com/Iz4bel4/ImageUploader/assets/112544496/cea8ea57-118b-45c4-8219-065b5422162e)

You have to click "Authorize" button in the top right corner.
Find "tokenAuth" section and paste their your token but in a format "Token {your token here}" (for example "Token 1234567890")

![AddingToken1](https://github.com/Iz4bel4/ImageUploader/assets/112544496/711c366f-c06a-4662-ae6a-8a27edf624fa)

Click Authorize

![AddingToken2](https://github.com/Iz4bel4/ImageUploader/assets/112544496/22c4f565-ae91-4db4-8726-1ab5983c5da6)

Done!

Now you can test API calls. Try changing your user tiers to different ones to see what is going on.

Just to ensure, that eveyrthing is OK, let's get throught it!

# Adding Images
You can add images using this POST call. It will return to you links, that you should get to download your image.
The only exception here is "Expirational Link", which COULD BE returned here, as well but got added to different method.

![BasicPostCall](https://github.com/Iz4bel4/ImageUploader/assets/112544496/15051a27-9b92-4845-aca5-c19c36f1ae1b)

IN MY OPINION ALL LINKS SHOULD BE ENCRYPTED, BUT NOT SURE IF IT IS REQUIRED SO IT WAS NOT IMPLEMENTED IN THIS "DEBUG" AND "DIRTY" CASE 

These should be your reponses based on your User tier setup:
For BASIC user tier

![UserTierSetToBasic](https://github.com/Iz4bel4/ImageUploader/assets/112544496/7609fbfc-7819-49eb-9ea1-2183c5631f7b)

You got only 200px height thumbnail

![BasicResponse1](https://github.com/Iz4bel4/ImageUploader/assets/112544496/e37e20cb-675f-4de2-9534-98f1e89be252)

Which looks like, that:

![BasicResponse2](https://github.com/Iz4bel4/ImageUploader/assets/112544496/09742e08-8aca-4070-8012-daf47864b137)

For PREMIUM/ENTERPRISE user tier

![UserTierSetToPremium](https://github.com/Iz4bel4/ImageUploader/assets/112544496/29b0059d-e6c8-47e2-b9b6-b5e87fcd3714)

You got 200px, 400px height thumbnails and an original image links

![PremiumPostResult1](https://github.com/Iz4bel4/ImageUploader/assets/112544496/e48f84e0-4ae3-4bdb-a0f4-ceb3eee5f388)

400px:

![Thumb400](https://github.com/Iz4bel4/ImageUploader/assets/112544496/7d88a260-cdff-4e46-827c-46f956fcf04c)

Original Image:

![Original](https://github.com/Iz4bel4/ImageUploader/assets/112544496/0b932a9e-88c6-4e37-88fe-20b8f090ef2b)

There are of course some validations:

![ValidationPost1](https://github.com/Iz4bel4/ImageUploader/assets/112544496/fba7f867-0f81-4590-9d85-dfd8190aa4b5)

![ValidationPost2](https://github.com/Iz4bel4/ImageUploader/assets/112544496/05b8bd95-30d8-4806-91bc-2d5f4843033d)

# Getting a list of images
You can list all of your (as a USER) images. It will result in getting all your download links for all images:

![BasicListGetCall](https://github.com/Iz4bel4/ImageUploader/assets/112544496/129a965e-8e0a-4a1c-adf8-46fca8bc99d9)

Basic tier user response:

![BasicListResponse1](https://github.com/Iz4bel4/ImageUploader/assets/112544496/d377c022-c22f-44f1-8d0f-8e167a013494)

Premium/Enterprise tier user response:

![PremiumList](https://github.com/Iz4bel4/ImageUploader/assets/112544496/1c21592f-bc66-4c4c-a1a2-d7dfa7f8199c)

# Getting single image links
You can additionally get DETAILED image links, by passing it's ID:

![GetDetail](https://github.com/Iz4bel4/ImageUploader/assets/112544496/f0799856-862c-4b67-8c00-097e331ff135)

Basic tier user response:

![BaseGetDetail](https://github.com/Iz4bel4/ImageUploader/assets/112544496/4c70edf4-4d32-4cc7-984e-d194d53ca6f8)

Premium/Enterprise tier user response:

![PremiumDetail](https://github.com/Iz4bel4/ImageUploader/assets/112544496/80315634-7e90-4737-852a-e494e5ccdfe1)

There are some validations:
For inappropriate ID:

![ValidationGetDetail1](https://github.com/Iz4bel4/ImageUploader/assets/112544496/0c731c72-a683-46d8-865f-28ba0a14c12a)

![ValidationDetail2](https://github.com/Iz4bel4/ImageUploader/assets/112544496/88231605-dd95-4dbe-a90d-054c6700a7e6)

When you want don't pass the expected type:

![ValidationDetail3](https://github.com/Iz4bel4/ImageUploader/assets/112544496/258ed8a8-3149-4caf-b5d5-bdb03ab522c1)

When you want someone's else image:

![NIEMABOTONIEON](https://github.com/Iz4bel4/ImageUploader/assets/112544496/2afec7d1-9f9a-4fab-8a5e-df54b5511899)

# Expiring links
You can get an original image link, which can expire after certain amount of time, by using this detailed call:
(Number of seconds should be between 300 and 30000, by code)

![ExpirationCall](https://github.com/Iz4bel4/ImageUploader/assets/112544496/6df53673-ac7d-48df-9ae5-221b54290c11)

When you are Basic/Premium user you will get something like this:

![ExpirationalValidationResult1](https://github.com/Iz4bel4/ImageUploader/assets/112544496/33bf212e-76b9-4e73-88e2-8d1b16b56bb7)

But as an Enterprise user your response will look like that:

![EnterpriseDelayed](https://github.com/Iz4bel4/ImageUploader/assets/112544496/34de5f14-416f-46f1-a3f4-51847e81ef70)

Which should result in getting an original image:

![Expirational1Good](https://github.com/Iz4bel4/ImageUploader/assets/112544496/be7e584d-87be-480d-9379-c412e4eb57fa)

Or no image if you are too late:

![LinkHasExpired](https://github.com/Iz4bel4/ImageUploader/assets/112544496/bafb3d91-df9a-4625-af9a-2bc1f4e77649)

There are a lot of validations here too:

![ExpirationalValidation7](https://github.com/Iz4bel4/ImageUploader/assets/112544496/a6cf70a7-359b-4daa-8fe5-d0a0eb813797)

![ExpirationalValidation8](https://github.com/Iz4bel4/ImageUploader/assets/112544496/4c1aaca4-57a0-4424-85b6-96a2f7b49e1a)

Or when passing wrong ID:

![ExpirationalValidationResult2](https://github.com/Iz4bel4/ImageUploader/assets/112544496/3201b0e9-1497-4c57-9203-7047ee86c639)

![ExpirationalValidation3](https://github.com/Iz4bel4/ImageUploader/assets/112544496/e04ad441-913f-426d-b166-6093411d7eaa)

Or wrong number:

![ExpirationalValidation4](https://github.com/Iz4bel4/ImageUploader/assets/112544496/8440842f-d189-43d5-bdac-4a49023be995)

![ExpirationalValidation6](https://github.com/Iz4bel4/ImageUploader/assets/112544496/cb3254f3-e70e-4d46-857f-71517f354298)

![Exp irationalValidation5](https://github.com/Iz4bel4/ImageUploader/assets/112544496/1eeca64c-4edb-47d7-bf6e-b923d284755b)

Or when you want someone's else image:

![NIEMABOTONIEON](https://github.com/Iz4bel4/ImageUploader/assets/112544496/dae25b6e-624b-4d15-9866-f935dde98d36)

# Tests
What more, there are 33 different tests implemented:
Just call in console:
docker-compose run --rm app sh -c "python manage.py test"
and see for youself.

![TestsDone](https://github.com/Iz4bel4/ImageUploader/assets/112544496/bf823a1e-702f-4167-a090-2d8528faf97f)

Tests contain:
- Admin user lists, page editing, creating tests.
- Waiting for a database.
- Creating a user with the proper email, email normalization, trying to create a user without an email.
- Creating new graphic and testing their name uuids.
- Creating a user, with existing email, with too short password.
- Creating a token for a user, its bad credentials, not finding an email, blank passowrd and unathorized user.
- Retrieving user profile.
- Listing all user's graphics.
- Getting single and multiple graphics.
- Trying to get someone's else image.
- Getting and not getting an original link, thumbnails and expirational links based on tier and values.
