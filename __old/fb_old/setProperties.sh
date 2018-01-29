curl -X POST -H "Content-Type: application/json" -d '{
  "greeting":[
    {
      "locale":"default",
      "text":"Hello {{user_first_name}}!"
    },
  ],

  "get_started":{ "payload":"GET_STARTED" },

  "persistent_menu":[
    {
      "locale":"default",
      "composer_input_disabled": true,
      "call_to_actions":[
        {
          "title":"Show Coinbase-Coindelta",
          "type":"postback",
          "payload":"Coinbase-Coindelta"
        }
      ]
    }
  ]
}' "https://graph.facebook.com/v2.6/me/messenger_profile?access_token=EAACQpBHVGckBAFstCjzTLaKMAaMxqtvP6m2L5o1yw3YKI7Jv6AH3ti7KfhZBfWmqDny7ovZAqqVKRbVWEvqkezjbyjTsQeN5mHMH4ZBoQStA5Hr4Qnhfps7AIvQIUxRf5EZCZCBogM5vTws8GUd348CfwNes3nOHBzENvtNdHwQZDZD"
