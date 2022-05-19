Feature: SignalR
    Scenario: Check that all hubs returned a response
        When We initialize a signalR
        Then signalR has to return response at all hubs
