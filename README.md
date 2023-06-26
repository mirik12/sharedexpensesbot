
**Shared Expenses Bot**
Shared Expenses Bot is a Telegram bot designed to solve the problem of managing expenses within a group or family, particularly when the members are dispersed across different locations. The idea for this bot originated from the need to address the challenges that arise when individuals or families living in various parts of the world, often as a group, need to track shared expenses such as groceries, hygiene products, and other shared items.

**Problem**
The problem arises from the complexity of tracking and allocating expenses within a group or family when the members are geographically separated. This situation can lead to difficulties, misunderstandings, and potential financial issues when it comes to calculating and managing shared expenses.

**Solution**
The Shared Expenses Bot offers a convenient solution for recording and managing expenses within a group or family. With this bot, users can:

Record expenses, including the amount, date, and description.
Track the overall budget of the group or family.
Receive notifications about new expenses and updates to the budget.
This bot facilitates clear communication and efficient expense management among the group or family members, ensuring transparency and reducing the potential for conflicts or misunderstandings.

**Technologies**
The project utilizes the following technologies and tools:

Python: Used for bot development and interaction with the database.
Kubernetes and Docker: Employed for containerization and deployment of the project.
Monitoring: Implemented for performance monitoring and issue detection.
CI/CD with GitHub Actions: Enables automated build, testing, and deployment processes.
Flux or Argo CD: Facilitates continuous delivery and automatic deployment in Kubernetes.


## Bot Functionality

1.  Registration and Group Creation: User Miroslav can register in the bot and create a new group. He can add other participants, such as Natasha, Sasha, Valentina, and Yana, to this group.
    
2.  Adding Expenses: Miroslav can add expenses through the bot. After selecting a command (e.g., /start), a menu is displayed with options, including "Add Expense." After entering the expense amount (digits only), the bot asks Miroslav to confirm the amount. If the amount is entered correctly, the bot prompts for the expense location (description). Information about the expense (name, amount, location, time, date) is stored in the database.
    
3.  Personal Expense Statistics: Miroslav can view statistics of his personal expenses through the "Personal Expense Statistics" option. This includes the total amount spent, graphs or charts showing the change in expenses over time, and more.
    
4.  Group Expense Statistics: The bot provides the option to view overall expense statistics for the group through the "Group Expense Statistics" option. This includes the total group expenditure, distribution of expenses by categories, graphs or charts, and more.
    
5.  Authentication and Privacy: Each user has their own account, and expense data is private. Users can only access their own personal expenses and statistics.


**Contribution**
Contributions to the project are welcome! If you have any ideas, suggestions, or would like to collaborate, please fork the repository and create a Pull Request with your proposed changes.
