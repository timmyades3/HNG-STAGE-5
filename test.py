import asyncio
from deepgram import Deepgram
# async def transcribe_audio():
#         Deepgram_api_key = "2930598b2500b43928ae66bbaf437a843b8c48a4"
#         dg_client = Deepgram(Deepgram_api_key)
#         source = {'buffer': 'new.mp3', 'mimetype': 'audio/mp3'}
#         response = await dg_client.transcription.prerecorded(source)
#         result = response['results']['channels'][0]['alternatives'][0]['transcript']
#         return result

# asyncio.run(transcribe_audio())




async def main():
        
    deepgram = Deepgram("2930598b2500b43928ae66bbaf437a843b8c48a4")
    audio = open('new.mp3', 'rb')
    source = {
      'buffer': audio,
      'mimetype': 'audio/mp3'
    }

    # Send the audio to Deepgram and get the response
    response = await asyncio.create_task(
        deepgram.transcription.prerecorded(
        source,
        {
            'smart_format': True,
            'model': 'nova',
        }
        )
    )
    print(response["results"]["channels"][0]["alternatives"][0]["transcript"])
    
if __name__ == '__main__':
    asyncio.run(main())