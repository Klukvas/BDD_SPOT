from GRPC.Сampaigns import campaigns
from datetime import datetime
import json
from enum import IntEnum


class ConditionWeightEnum(IntEnum):
    KYCCondition = 1
    DepositCondition = 2
    TradeCondition = 3
    ConditionsCondition = 99


class CampaignWorker:

    def __init__(self):
        self.campaign = None
        self.criteria_steps = {}
        self.condition_steps = {}
        self.rewards = {}

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

    def get_rewards(self, rewards: list) -> dict:
        for item in rewards:
            if 'Type' not in item.keys():
                item['Type'] = 'FeeShareAssignment'
            self.rewards[item['Type']] = item['Parameters']
        return self.rewards

    @staticmethod
    def sort_dict_by_field(dict_to_sort: dict, key_field_sort: str) -> dict:
        list_d = list(dict_to_sort.items())
        list_d.sort(key=lambda i: i[1][key_field_sort])
        sorted_dict = {k[0]: k[1] for k in list_d}
        return sorted_dict

    def get_condition_steps(self):
        for condition in self.campaign[0]['Conditions']:
            if 'Type' not in condition.keys():
                condition['Type'] = 'KYCCondition'
            self.condition_steps[condition['Type']] = {'weight': ConditionWeightEnum[condition['Type']].value}
            self.condition_steps[condition['Type']]['Steps'] = condition['Parameters']
            if 'Rewards' in condition.keys():
                self.condition_steps[condition['Type']]['Rewards'] = self.get_rewards(condition['Rewards'])
            else:
                self.condition_steps[condition['Type']]['Rewards'] = {}
        self.condition_steps = CampaignWorker.sort_dict_by_field(self.condition_steps, 'weight')
        return self.condition_steps

    def main(self):
        self.find_campaign_by_id('7d132d2ac7c34b7ca787db703c9b8ee2')
        a = self.get_condition_steps()
        return a


if __name__ == "__main__":
    c = CampaignWorker().main()
    print(c)
