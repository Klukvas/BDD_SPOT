from GRPC.Сampaigns import campaigns
from datetime import datetime
import json


class CampaignWorker:

    def __init__(self):
        self.campaign = None
        self.criteria_steps = {}
        self.condition_steps = {}

    def find_campaign_by_id(self, cmp_id: str):
        try:
            all_campaigns = json.loads(
                campaigns.get_all_campaigns()
            )['Campaigns']
        except Exception as err:
            raise Exception(f"Something went wrong with getting all campaigns. Error: {err}")
        self.campaign = list(
            filter(
                lambda campaign: campaign['Id'] == cmp_id,
                all_campaigns
            )
        )
        return self.campaign

    def get_criteria_steps(self):
        for criteria in self.campaign[0]['CriteriaList']:
            if 'CriteriaType' not in criteria.keys():
                criteria['CriteriaType'] = 'RegistrationType'
            if criteria['CriteriaType'] == 'KycType':
                for param_name, param_val in criteria['Parameters'].items():
                    if param_val:
                        if 'KYC' in self.criteria_steps.keys():
                            self.criteria_steps['KYC'].append(param_name)
                        else:
                            self.criteria_steps['KYC'] = [param_name]
            elif criteria['CriteriaType'] == 'RegistrationType':
                if criteria['Parameters']['CountriesList'] != "":
                    raise Exception('Can`t test campaign if CountriesList criteria filled')
                if criteria['Parameters']['DateParam'] != "":
                    try:
                        reg_date = datetime.strptime(criteria['Parameters']['DateParam'], '%m/%d/%Y').date()
                    except Exception as err:
                        raise Exception(f"""
                            Can not convert DateParam. 
                            Expected format: %m/%d/%Y. 
                            Returned: {criteria['Parameters']['DateParam']}
                            Error: {err}
                        """)
                    today_date = datetime.today().date()
                    if not today_date > reg_date:
                        raise Exception(f"Date in campaign: {reg_date} is greater than date today({today_date})")
            elif criteria['CriteriaType'] == 'ReferralType':
                if criteria['Parameters']['HasReferrer']:
                    self.criteria_steps['HasReferrer'] = True
        return self.criteria_steps

    def get_rewards(self, rewards: list, condition_type: str):
        for item in rewards:
            if item['Type'] == 'ReferrerPaymentAbsolute':
                if 'Rewards' in self.condition_steps[condition_type].keys():
                    pass
                else:
                    self.condition_steps[condition_type]['Rewards'] = item['Parameters']

    def get_condition_steps(self):
        for condition in self.campaign['Conditions']:
            if condition['Type'] == 'KYCCondition':
                self.condition_steps['KYCCondition'] = {}
                for param_name, param_val in condition['Parameters'].items():
                    if param_val:
                        if 'Steps' in self.condition_steps['KYCCondition'].keys():
                            self.condition_steps['KYCCondition']['Steps'].append(param_name)
                        else:
                            self.condition_steps['KYCCondition']['Steps'] = [param_name]

    def main(self):
        self.get_criteria_steps()
        return self.criteria_steps


if __name__ == "__main__":
    cmp = {}
    c = CampaignParser(cmp).main()
    print(c)
