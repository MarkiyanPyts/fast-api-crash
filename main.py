from fastapi import FastAPI

api = FastAPI()

all_todos = [
    {'todo_id': 1, 'todo_name': 'Sports', 'todo_description': 'Play football'},
    {'todo_id': 2, 'todo_name': 'Music', 'todo_description': 'Listen to music'},
    {'todo_id': 3, 'todo_name': 'Study', 'todo_description': 'Study for exams'},
    {'todo_id': 4, 'todo_name': 'Shopping', 'todo_description': 'Buy groceries'},
]

@api.get("/")
def index():
    return {"message": "Hello from fast-api-crash!"}

@api.get('/todos/{todo_id}')
def get_todo(todo_id: int):
    for todo in all_todos:
        if todo['todo_id'] == todo_id:
            return todo
    return {"error": "Todo not found"}

@api.get('/todos')
def get_todos(first_n: int = None):
    if first_n is not None:
        return {"todos": all_todos[:first_n]}
    else:
        return {"todos": all_todos}
    
@api.post('/todos')
def create_todo(todo: dict):
    new_todo_id = max(todo['todo_id'] for todo in all_todos) + 1
    
    new_todo = {
        'todo_id': new_todo_id,
        'todo_name': todo['todo_name'],
        'todo_description': todo['todo_description']
    }

    all_todos.append(new_todo)
    return {"message": "Todo created successfully", "todo": new_todo}

@api.put('/todos/{todo_id}')
def update_todo(todo_id: int, updated_todo: dict):
    for i, todo in enumerate(all_todos):
        if todo['todo_id'] == todo_id:
            all_todos[i] = {**todo, **updated_todo}
            return {"message": "Todo updated successfully", "todo": all_todos[i]}
    return {"error": "Todo not found"}

@api.delete('/todos/{todo_id}')
def delete_todo(todo_id: int):
    for i, todo in enumerate(all_todos):
        if todo['todo_id'] == todo_id:
            del all_todos[i]
            return {"message": "Todo deleted successfully"}
    return {"error": "Todo not found"}
