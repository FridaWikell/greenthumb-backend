# GreenThumb Hub - Backend

![image of site](link to image) - use an image from AmIResponsive that shows the site on multiple devices

## Introduction

This is the backend of the project GreenThumb Hub. You can find the frontend repository [here](https://github.com/FridaWikell/greenthumb-front).

The project is about creating a social media, a hub, for all gardeners. The purpose is to show other green fingered fellows how your garden is progressing, to ask for advice and questions or just have a fun time and find new friends with the same hobby as yourself. 

## Table of Contents

## User Experience

### User Goals

The user goal is to be able to share the interest and hobby with other green fingered people. They should be able to communicate and learn from each others knowledge.

### Site Owner Goals

The site owner goal is to provide a place where the green fingers can grow and crack in bloom.

### Epics & User Stories

To view all epics and user stories for the backend are collected at a project board [here](https://github.com/users/FridaWikell/projects/7).

#### Epics

[User authentication](https://github.com/users/FridaWikell/projects/7/views/1?pane=issue&itemId=60174807)  
As a new or returning user, I would like to securely log in or change my password, so that I can access my personalized account securely and maintain my privacy.

[User profile management](https://github.com/users/FridaWikell/projects/7/views/1?pane=issue&itemId=60175794)  
As a registered user, I would like to update my profile information including my profile image and username, so that my profile reflects my current preferences and identity.

[Content management](https://github.com/users/FridaWikell/projects/7/views/1?pane=issue&itemId=60177794)  
As a user, I would like to publish and manage posts with text and images, so that I can share and express my thoughts, experiences, and creative content with the community.

[Social interaction](https://github.com/users/FridaWikell/projects/7/views/1?pane=issue&itemId=60178790)  
As a user, I would like to interact with other users' content through likes and follow their profiles, so that I can engage with the community and stay updated on content from users I am interested in.

[Participation in polls](https://github.com/users/FridaWikell/projects/7/views/1?pane=issue&itemId=60180110)  
As a user, I would like to participate in polls, so that I can express my opinions and engage with interactive content on the platform.

#### User Stories

All user stories are labeled with must have, should have, could have or won't have, depending on prioritization according to MoSCoW prioritization. Each of all user stories are also labeled with a point. The point is an estimate in how long time it will take to finish the acceptance criterias in the user story. All acceptance criterias are presented in each user story at the project board.

User stories:

[User login](https://github.com/users/FridaWikell/projects/7/views/1?pane=issue&itemId=60175146)  
As a user, I would like to be able to log in to my account using my credentials, so that I can access my personalized experience on the platform.

[User password change](https://github.com/users/FridaWikell/projects/7/views/1?pane=issue&itemId=60175628)  
As a registered user, I would like to change my password, so that I can ensure my account's security.

[Update profile image](https://github.com/users/FridaWikell/projects/7/views/1?pane=issue&itemId=60176260)  
As a registered user, I would like to update my profile image, so that I can keep my profile up-to-date.

[Update username](https://github.com/users/FridaWikell/projects/7/views/1?pane=issue&itemId=60177301)  
As a registered user, I would like to change my username, so that I can update my identity on the platform.

[Publish posts with images](https://github.com/users/FridaWikell/projects/7/views/1?pane=issue&itemId=60178550)  
As a user, I would like to publish posts with images, so that I can share content with others.

[Like posts](https://github.com/users/FridaWikell/projects/7/views/1?pane=issue&itemId=60179228)  
As a user, I would like to like posts made by others, so that I can engage with content that I find appealing.

[Follow users](https://github.com/users/FridaWikell/projects/7/views/1?pane=issue&itemId=60179916)  
As a user, I would like to follow other users, so that I can keep up with their posts and activities on the platform.

[Participate in polls](https://github.com/users/FridaWikell/projects/7/views/1?pane=issue&itemId=60180465)  
As a user, I would like to participate in polls, so that I can express my opinion on different topics.

## Design

### Entity-Relationship Diagram - ERD

The ERD’s for the project is presented below.

SÄTT IN ERD!


## Testing

### Validation of Code
Insert screenshots of HTML, CSS and any other code files being tested in the relevant code validator - CSS validator might not validate newer CSS syntax - be careful to read and fully understand why it is giving you an error.

### Automated Testing

A total of 34 tests were written for all apps. Below, the sum for each app is presented and linked to each app.

[Comments](https://github.com/FridaWikell/greenthumb-backend/blob/main/comments/tests.py)

![Screenshot of test result for comments](doc/tests-comments.webp)

[Followers](https://github.com/FridaWikell/greenthumb-backend/blob/main/followers/tests.py)

![Screenshot of test result for followers](doc/tests-followers.webp)

[Likes](https://github.com/FridaWikell/greenthumb-backend/blob/main/likes/tests.py)

![Screenshot of test result for likes](doc/tests-likes.webp)

[Polls](https://github.com/FridaWikell/greenthumb-backend/blob/main/polls/tests.py)

![Screenshot of test result for polls](doc/tests-polls.webp)

[Posts](https://github.com/FridaWikell/greenthumb-backend/blob/main/posts/tests.py)

![Screenshot of test result for posts](doc/tests-posts.webp)

[Profiles](https://github.com/FridaWikell/greenthumb-backend/blob/main/profiles/tests.py)

![Screenshot of test result for profiles](doc/tests-profiles.webp)

### Manual Testing

| Feature being tested | Expected Outcome | Testing Performed | Actual Outcome | Result (Pass or fail) |
| -------------------- | ---------------- | ----------------- | -------------- | --------------------- |
| Sign up | New user gets signed up | Enter requested information in sign up form | 
| Sign up with same username | User can’t sign up when they try username already in use | Try to sign up with a username already in use | 
| Log in | User gets logged in with correct user credentials | Enter valid user information | enter details here | enter details here |
| Password change | Password updates when the same password is entered twice | Enter new password and confirm the password in change password form |
| Password change - fail | Password doesn’t updates if you don’t write the same password twice in change password form |

| Feature being tested | Expected Outcome | Testing Performed | Actual Outcome | Result (Pass or fail) |
| -------------------- | ---------------- | ----------------- | -------------- | --------------------- |
| Change profile image | The profile image changed at all places when save is pressed | Change profile image, check profile image at all places |
| Update username | The username is changed at all places when save is pressed | Change username, check username at all places |
| Update username - fail | Username doesn’t update when the user tries to update to a username already in use | Try to update username to an username already in use |
| Update username - warning | The user gets a warning that the username they try to change to already is in use | Try to update username to an username already in use |

| Feature being tested | Expected Outcome | Testing Performed | Actual Outcome | Result (Pass or fail) |
| -------------------- | ---------------- | ----------------- | -------------- | --------------------- |
| Upload a post with an image | The post is submitted when an image, text and content is applied | Add a post with image, title and content | 
| Upload a post without an image | The post is submitted when text and content is applied | Add a post with title and content |
| Error message for large images | When an image over 2 MB is uploaded, an error message is shown | Upload a large image, over 2 MB in size | 
| Change image before creating post | When an image is uploaded, the user can change the image and upload a new image before submitting the post | Upload an image, change image and upload a new |

| Feature being tested | Expected Outcome | Testing Performed | Actual Outcome | Result (Pass or fail) |
| -------------------- | ---------------- | ----------------- | -------------- | --------------------- |
| Like post | When the like button is pressed, a like is registered and the number of likes increases by one | Find a post, press like button | 
| Unlike post | When the like button at an already liked post is pressed, the like is taken back and the number of likes decreases by one | Find a already liked post, press like button |
| Follow user | When the follow button is pressed, the user is followed and its post is visible in “plant friends” | Find a user, press follow and view to be sure its posts are visible in plant friends | 
| Follow user - button change | When the follow button is pressed, it changes to become an unfollow button | Find a user, press follow and watch the button content change |
| Unfollow user | When the unfollow button is pressed, the user is unfollowed and its post isn’t visible in “plant friends” | Find a user, press unfollow and view to be sure its posts aren’t visible in plant friends | 
| Unfollow user - button change | When the unfollow button is pressed, it changes to become a follow button | Find a user, press unfollow and watch the button content change |


| Feature being tested | Expected Outcome | Testing Performed | Actual Outcome | Result (Pass or fail) |
| -------------------- | ---------------- | ----------------- | -------------- | --------------------- |
| Post a question | When question and answers are filled out and submit button is pressed, the questions is posted | Write a question, add answers, press submit | 
| Delete a question | When the user is logged in, they can delete they own questions | Press delete at their own question | 
| View votes | View number of votes at each answer | Press view result | 



You should have tests for every section of every page.. individually.

## Technologies Used

Detail what technologies you used. So what code languages, what frameworks, libraries, what software did you use to develop the site - Balsamic for your wireframes, Figma for a mockup?

## Deployment

Detail how to clone the repository, how to fork the repository - how to run the site locally and how to deploy it.


## Credits

You need to credit where you got anything for your site from.. where are the images from, are they all from the same site? where did you get the content from, if you wrote it yourself, did you fact check anywhere? did you get code from anywhere? if so, it needs to be clearly marked in both the code and the readme.

## Acknowledgements
Any special acknowledgements you'd like to leave

Back to top link to return to the top of the readme.
