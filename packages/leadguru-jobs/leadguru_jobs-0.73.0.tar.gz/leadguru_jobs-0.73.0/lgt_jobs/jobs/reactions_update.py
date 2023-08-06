from abc import ABC
from datetime import datetime, timedelta
from lgt.common.python.lgt_logging import log
from lgt.common.python.slack_client.web_client import SlackWebClient, get_system_slack_credentials
from pydantic import BaseModel
from lgt_data.mongo_repository import LeadMongoRepository, BotMongoRepository, DedicatedBotRepository
from ..basejobs import BaseBackgroundJobData, BaseBackgroundJob

"""
Update messages reactions
"""


class UpdateReactionsJobData(BaseBackgroundJobData, BaseModel):
    days: int = 1  # update messages for the last day by default


class UpdateReactionsJob(BaseBackgroundJob, ABC):
    @property
    def job_data_type(self) -> type:
        return UpdateReactionsJobData

    def exec(self, data: UpdateReactionsJobData):
        bots = BotMongoRepository().get()
        from_date = datetime.utcnow() - timedelta(days=data.days)
        like_name = '+1'

        leads_repository = LeadMongoRepository()
        leads = list(leads_repository.get_list(0, 0, from_date=from_date))
        for lead in leads:
            creds = get_system_slack_credentials(lead, bots)

            if not creds:
                log.warning(f"Lead: {lead.id}, bot credentials are not valid")

            client = SlackWebClient(creds.token, creds.cookies)
            message_data = client.get_reactions(lead.message.channel_id, lead.message.slack_options['ts'])
            if not message_data['ok']:
                continue

            message = message_data.get('message')
            if not message:
                continue

            replies = message.get('reply_count')
            lead.replies = replies if replies else 0

            reactions_data = message.get('reactions')
            reactions = reactions_data if reactions_data else []
            for reaction in reactions:
                if reaction["name"] == like_name:
                    lead.likes = reaction["count"]
                else:
                    lead.reactions += 1

            leads_repository.update(lead.id, replies=lead.replies, likes=lead.likes, reactions=lead.reactions)
