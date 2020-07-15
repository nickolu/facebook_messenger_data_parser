# Manchat Data Processing
For python 3

To run this, open the main.py and edit the report with what you'd like to build and run

Then run `python main.py` in your terminal.


## Oh yeah

In order for this to work, you need to load the json files into the facebook and hangouts directories under chat_data. They should look like this:

`chat_data/facebook/my_json_data.json`
`chat_data/hangouts/my_hangouts_data.json`

The report.run() method will iterate through any json files in those directories, so make sure only the files you want to iterate through are located there. The files should be formateed like so:

```
{
    "messages": [
        {
            "sender_name": "Mary Poppins",
            "timestamp_ms": 1523423424323,
            "content": "A spoonful of sugar helps the medicine go down in the most delightful way"
        }
    ]
}
```

