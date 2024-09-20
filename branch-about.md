Branches in Git are needed to:
Several programmers can work on the same project or file at the same time without interfering with each other.
Test experimental features. In order not to damage the main project, a new branch is created specifically for experiments. 
If the experiment is successful, the changes from the experimental branch are transferred to the main one. 
If not, the new branch is deleted, and the project remains untouched.

1) How to create a branch
To create a new branch in Git, follow these steps:
Go to your project folder: cd /path/to/your/project.
Create a new branch: git checkout -b <new_branch_name>.
2) To switch to a branch in Git, use the command: git checkout your-branch
3) To push a branch to the server using the git push command, follow these steps:
Create a link between the remote and local repository using the command: git remote add <repo_name> link.
Save the changes using the git commit command.
In the terminal, enter the command: git push origin <branch>.
