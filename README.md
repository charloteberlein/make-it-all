# Team 2

## Repository structure
```
src/
    mockData/
        users.json — Pre-filled test users and rol
        tasks.json — Sample to-dos with assignee task counts
        topics.json — Sample knowledge base topics (e.g., Printing, Software Dev)
        posts.json — Sample posts with verified/unverified 
    components/
        LoginModal.tsx — UI that simulates login and @make-it-all.co.uk domain check
        ManagerDashboard.tsx — Renders workload metrics and task count charts from tasks.json
        TaskBoard.tsx — Personal vs. Team/Project task lists
        KnowledgeBase.tsx — Filterable post feed with topic tags
    App.tsx — Main application layout and view route
README.md
```