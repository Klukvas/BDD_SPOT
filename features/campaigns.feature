# Created by andrey.p s
@campaign
Feature: Campaigns
    # Проверка кампаний просходи по следующему сценарию:
    #     Получаем камнанию, которая должна быть активной
    #     Проходим все необходимые критерии. !Если в критерии указана страна - тесты будут зафейлены
    #     Проверка, что у пользователя появилась кампания в контексте
    #     Пользователь проходит небюходимые критерии. !Если в критерии есть депозит не в usd - критерий не будет пройден
    #     Пользователь получает награды за пройденные критерии. Если награда - FeeShareAssignment - проверка не будет выполнена
    Scenario Outline: Check campaign
        Given User gets campaign with id: <cmp_id>
        When User passed all criteria in campaign
        Then User has campaign in the context
        When User passed conditions
        Then User gets some reward
    Examples:
        | cmp_id                           |
        | 7d132d2ac7c34b7ca787db703c9b8ee2 |

