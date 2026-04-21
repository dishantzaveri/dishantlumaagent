import logging
import asyncio
from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentSession, Agent
from livekit.plugins import openai, deepgram, silero
from livekit.plugins.openai import tts as openai_tts
from knowledge_base import get_system_prompt

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dishant-twin")


class DishantTwin(Agent):
    def __init__(self):
        super().__init__(instructions=get_system_prompt())

    async def on_enter(self):
        await self.session.say(
            "Hey! I'm Dishant's AI twin — what brings you to the portfolio today?",
            allow_interruptions=True,
        )


async def entrypoint(ctx: agents.JobContext):
    logger.info(f"Joining room: {ctx.room.name}")
    await ctx.connect()

    session = AgentSession(
        stt=deepgram.STT(model="nova-2", language="en-US"),
        llm=openai.LLM(model="gpt-4o-mini", temperature=0.7),
        tts=openai_tts.TTS(model="tts-1", voice="onyx"),
        vad=silero.VAD.load(),
    )

    await session.start(room=ctx.room, agent=DishantTwin())
    logger.info("Session live — listening for visitor...")
    await asyncio.sleep(float("inf"))


if __name__ == "__main__":
    agents.cli.run_app(
        agents.WorkerOptions(entrypoint_fnc=entrypoint)
    )
