import uuid

from fastapi import FastAPI,HTTPException,File,UploadFile,Depends,Form
#
from schemas import Postcreate,PostResponse,UserRead,UserCreate,UserUpdate
#
from db import Post,get_async_sessionl,create_db_and_tables,User

from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
from images import imagekit
    # ,response
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
import shutil
import os
import uuid
import tempfile
from users import auth_backend,current_active_user,fastapi_users

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 2. This runs when your app STARTS UP
    await create_db_and_tables()

    yield  # 3. The app is running here!

    # 4. (Optional) Anything written here runs when the app SHUTS DOWN
app=FastAPI(lifespan=lifespan)

app.include_router(fastapi_users.get_auth_router(auth_backend),prefix="/auth/jwt",tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead,UserCreate),prefix="/auth",tags=["auth"])
app.include_router(fastapi_users.get_reset_password_router(),prefix="/auth",tags=["auth"])
app.include_router(fastapi_users.get_verify_router(UserRead),prefix="/auth",tags=["auth"])
app.include_router(fastapi_users.get_users_router(UserRead,UserUpdate),prefix="/auth",tags=["auth"])


@app.post("/upload")
async def upload_file(
        file: UploadFile = File(...),
        user:User=Depends(current_active_user),
        caption: str = Form(...),
        session: AsyncSession = Depends(get_async_sessionl)
):

    temp_file_path=None

    try:
        with tempfile.NamedTemporaryFile(delete=False,suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file_path=temp_file.name
            shutil.copyfileobj(file.file,temp_file)
        upload_result=imagekit.upload_file(
            file=open(temp_file_path,"rb"),
            file_name=file.filename,
            options=UploadFileRequestOptions(
                use_unique_file_name=True,
                tags=["backend-upload"]

            )
        )
        if upload_result.response_metadata.http_status_code==200:
            post = Post(
                user_id=user.id,
                caption=caption,
                URL=upload_result.url,
                filename=upload_result.name,
                file_type="video" if file.content_type.startswith("video/") else "image",
            )

            session.add(post)
            await session.commit()
            await session.refresh(post)
            return post
    except Exception as e:
        pass
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()
        #to clean file object after we finish
@app.get("/refresh")
async def get_feed(
        session:AsyncSession=Depends(get_async_sessionl),
        user:User=Depends(current_active_user)
):
    result=await session.execute(select(Post))

    posts=[row[0]for row  in result.all()]
    result=await session.execute(select(User))
    users=[row[0]for row in result.all()]
    user_dict={u.id:u.email for u in users}
    posts_data=[]
    for post in posts:
        posts_data.append(
            {
                "id":str(post.id),
                "user_id":str(post.user_id),
                "caption":post.caption,
                "url":post.URL,
                "file_type":post.file_type,
                "filename":post.filename,
                "create_at":post.create_at.isoformat(),
                "is_owner":post.user_id==user.id,
                "email":user_dict.get(post.user_id,"Unknown")

            }
        )
    return {"posts":posts_data}
# .order_by(Post.created_at.desc()).filter_by()

@app.delete("/posts/{post_id")
async def delete_post(post_id:str, session:AsyncSession=Depends(get_async_sessionl)):
    try:
        post_uuid=uuid.UUID(post_id)
        result=await session.execute(select(Post).where(Post.id==post_uuid))
        post=result.scalars().first()

        if not post:
            raise HTTPException(status_code=404,detail="post not Found")
        if post.user_id != User.id:
            raise HTTPException(status_code=403,detail="not authorized to delete this post")
        await session.delete(post)
        await session.commit()
        return {"success":True,"message":"Post Delete successfuly"}
    except Exception as e:
        raise HTTPException(status_code=505,detail=str(e))



