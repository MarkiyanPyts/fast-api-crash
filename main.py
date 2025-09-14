from fastapi import FastAPI, HTTPException
from typing import Optional, List
from enum import IntEnum
from pydantic import BaseModel, Field

api = FastAPI()

class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class TodoBase(BaseModel):
    todo_name: str = Field(..., min_length=3, max_length=512, description="Name of the todo item")
    todo_description: str = Field(..., min_length=3, max_length=1024, description="Description of the todo item")
    priority: Priority = Field(Priority.LOW, example=Priority.LOW, description="Priority of the todo item")

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    todo_name: Optional[str] = Field(None, min_length=3, max_length=512, description="Name of the todo item")
    todo_description: Optional[str] = Field(None, min_length=3, max_length=1024, description="Description of the todo item")
    priority: Optional[Priority] = Field(None, example=Priority.LOW, description="Priority of the todo item")


class Todo(TodoBase):
    todo_id: int = Field(..., description="ID of the todo item")

all_todos = [
    Todo(todo_id=1, todo_name='Sports', todo_description='Play football', priority=Priority.HIGH),
    Todo(todo_id=2, todo_name='Music', todo_description='Listen to music', priority=Priority.LOW),
    Todo(todo_id=3, todo_name='Study', todo_description='Study for exams', priority=Priority.MEDIUM),
    Todo(todo_id=4, todo_name='Shopping', todo_description='Buy groceries', priority=Priority.LOW),
]

@api.get('/todos/{todo_id}', response_model=Todo)
def get_todo(todo_id: int):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@api.get('/todos', response_model=List[Todo])
def get_todos(first_n: int = None):
    if first_n is not None:
        return all_todos[:first_n]
    else:
        return all_todos
    
@api.post('/todos', response_model=Todo)
def create_todo(todo: TodoCreate):
    new_todo_id = max(todo.todo_id for todo in all_todos) + 1
    
    new_todo = Todo(
        todo_id=new_todo_id,
        todo_description=todo.todo_description,
        todo_name=todo.todo_name,
        priority=todo.priority
    )
    
    all_todos.append(new_todo)

    return new_todo

@api.put('/todos/{todo_id}', response_model=Todo)
def update_todo(todo_id: int, updated_todo: TodoUpdate):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            todo.todo_name = updated_todo.todo_name or todo.todo_name
            todo.todo_description = updated_todo.todo_description or todo.todo_description
            todo.priority = updated_todo.priority or todo.priority
            return {"message": "Todo updated successfully", "todo": todo}
    raise HTTPException(status_code=404, detail="Todo not found")

@api.delete('/todos/{todo_id}', response_model=Todo)
def delete_todo(todo_id: int):
    for i, todo in enumerate(all_todos):
        if todo.todo_id == todo_id:
            del all_todos[i]
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@api.get('/')
def root():
    return {"message": "Welcome to the Todo API!"}