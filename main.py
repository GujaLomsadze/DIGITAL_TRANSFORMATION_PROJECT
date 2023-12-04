import openai
from fastapi import FastAPI

from configs.load_config import get_config
from endpoints.conversation_endpoints import router as conversation_router
from endpoints.goals_endpoints import router as goals_router
from endpoints.gpt_endpoints import router as gpt_router
from endpoints.user_endpoints import router as user_router

# Initialize FastAPI app
app = FastAPI(
    title="StudyBuddy API V1",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

# Adding routers to App
app.include_router(gpt_router, prefix="/api/v1", tags=["ChatGPT"])
app.include_router(user_router, prefix="/api/v1", tags=["Users"])
app.include_router(goals_router, prefix="/api/v1", tags=["Goals/Tasks"])
app.include_router(conversation_router, prefix="/api/v1", tags=["Conversations"])

# Getting API key from config
_, openai_conf, _ = get_config()

# Set up OpenAI API key
openai.api_key = openai_conf["api_key"]

# Running ap Directly
if __name__ == "__main__":

    print("Starting the API...")

    import uvicorn
    from multiprocessing import cpu_count

    number_of_cores = cpu_count()

    if number_of_cores <= 6:
        raise OSError(f"You don't have enough number of cores to run the API. N of cores: {number_of_cores}")

    uvicorn.run(app, host="localhost", port=8000)
