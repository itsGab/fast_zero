from fast_zero.app import app
from fast_zero.routers import auth, users

app.include_router(users.router)
app.include_router(auth.router)
