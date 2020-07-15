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


## convert a raw hangouts json 

If you have a raw hangouts json file from takeout.google.com, it will not be formatted like the above example. There is a function in this repo to convert it for you. To use it, first place the file in the hangouts json directory under chat_data like so: `chat_data/hangouts/Hangouts.json`

Then, run the `simplify_hangouts_json_data` function in simplify_hangouts_json_data.py. The new file will also be placed in chat_data/hangouts/. Make sure to remove the original Hangouts.json otherwise the report runner will try to iterate that file and most likeley explode. You were warned!


