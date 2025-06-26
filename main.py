from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str 
    text: str
    is_done: bool 

items = []

@app.post("/items") 
def create_item(item: Item):
    items.append(item)
    return item

@app.get("/items", response_model=list[Item])
def list_items(limit: int = 10):
    return items[0:limit]

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id < len(items):
        items[item_id] = item
        return item
    else:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
        
@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    if item_id < len(items):
        item = items[item_id]
        return item
    else:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found") 

@app.delete("/items/{item_id}")
def delete_item(item_id: int) -> Item:
    if item_id < len(items):
        return items.pop(item_id)
    else:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found") 

