# QuestBoard
#### Video Demo:  <URL HERE>
#### Description:

QuestBoard is a website that allows a team of people to work together to keep track of multiple tasks for some larger project. After users have created an account, they are able to create tasks that need to be accomplished, "claim" tasks so that everyone knows who is in charge of what, and mark tasks complete. Finally, everyone is able to see at a glance what has been done so far.

Below I will introduce the files at use in the program along with what they do.

# tasks.db
This database has two tables, users and tasks. The users table keeps track of users and their hashed passwords, while the task database keeps track of tasks to be done, including their name, a description, their state (To Do, In Progress, or Completed), their handler (who is in charge of the task), and timestamps related to each step of the journey a task will go through.

# login.html
This page allows a user to log in. I based this page on the log in page used in the Finance assignment: no need to throw out good code!

# register.html
This page allows a user to register an account. This was also based on my work in the Finance assignment.

# layout.html
This page is the core of the site itself, as other html pages extend this one. I adjusted the Finance layout.html to fit the needs and scope of my project. 

# apology.html
The final page taken from Finance, this allows error messages to be shown to the user should they not follow the needs of the program.

# newtask.html
This page allows a user to create a new task. Two forms ask the user to provide a title for the task as well as a more in-depth description for what the task entails. This information, along with the time of creation of the task and the name of the user who made the task are saved in tasks.db.

# todo.html
This page displays tasks that have been created in the newtask.html page as cards that display the task name, description, date and time of creation, and who made the task. Each card has a button that allows a user to "claim" or take responsibility for completing that task.

It should be noted that I utilized chatGPT to help me get the layout of the cards, as I was unsure how to present the information in that way as opposed to as a table.

# inprogress.html
This page displays all tasks that have been claimed by users, showing their title, description, date and time they were claimed, and the handler of the task. If the user is using the same account that claimed the task, they are able to see a button that allows them to mark the task as complete. I didn't want other users to be able to accidentally change the state of a task that is someone else's responsibility.

I utilized chatGPT to learn the syntax needed to hide the Mark as Complete button from all users except the one who had claimed the task.

# completed.html
This page lists all completed tasks in a table, displaying the task title, description, handler, and date and time of completion.

I had initially wanted to also display the completed tasks as a stack of cards like all of the other pages. On further reflection, I opted on a table for a few reasons. The cards are great because they allocate a lot of space to the task description and have a strong visual break between tasks. It was also easy to implement the Claim and Mark as Complete buttons on each of those pages. 

However, the display for completed tasks, I figured, needed less visual space dedicated to descriptions and didn't need an integrated button: it is primarily a reflective page used to reference what's been done and to serve as a satisfying "victory lap" as a team can go over their accomplishments. For these reasons, I opted for a table instead of the cards.

# index.html
The homepage shows a user the tasks for which they personally are the handler. I wanted the user to have a place to reference only their own work, the intention being that a user clears their homepage before going to grab more in progress tasks or figuring out what needs to be created in todo.html.

I asked chatGPT the syntax needed to show the user only their own tasks.

# helpers.py
I appreciated the structure given to requiring logins and rendering apologies presented in Finance, so I adjusted the helpers.py file from that and brought it forward here.

# app.py
This file contains all of the logic for the above html pages. 

# styles.css
This file contains the CSS for all of my pages. I should note that one of the major visual differences I made to differentiate my work on QuestBoard from Finance was the implementation of a dark mode-esque visual style. In my experience darker backgrounds are much easier on my eyes. I should note that I used chatGPT to help me adjust the display of my task cards and my completed tasks table.

