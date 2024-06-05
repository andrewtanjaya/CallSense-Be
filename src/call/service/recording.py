import asyncio
import io
import logging
import os
import time
from uuid import UUID, uuid4

import requests
from aiohttp import ClientSession
from pydub import AudioSegment

from common.config import FIREBASE_STORAGE_BUCKET
from src.call.domain.entity import Call, CallDetail, Recording
from src.call.domain.interface import AbstractUnitOfWork
from src.call.service import sentiment as sentiment_service


def create_recording(
    uow: AbstractUnitOfWork,
    call_id: UUID,
    url: str,
):
    with uow:
        uow.recording.create(Recording(call_id=call_id, url=url))
        uow.commit()


def stream_audio_and_save_in_chunks(
    uow: AbstractUnitOfWork,
    call_id: UUID,
    url: str,
    source_file_format: str,
    output_file_format: str,
    chunk_duration=10,
):
    with uow:
        # Initialize the request
        response = requests.get(url, stream=True)

        if response.status_code != 200:
            logging.info(
                f"Failed to retrieve audio. HTTP Status Code: {response.status_code}"
            )
            return

        audio_data = io.BytesIO()
        start_time = time.time()
        chunk_index = 0
        output_folder = f"./audio_chunks/{call_id}"

        # Create output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        iteration = 0

        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                audio_data.write(chunk)

                # Calculate elapsed time
                elapsed_time = time.time() - start_time

                if elapsed_time >= chunk_duration:
                    # Reset start time for the next chunk
                    start_time = time.time()

                    # Convert raw audio data to an AudioSegment
                    audio_data.seek(0)
                    audio_segment = AudioSegment.from_file(
                        audio_data, format=source_file_format
                    )

                    # Export the AudioSegment to a file
                    file_name = f"{call_id}_{chunk_index}.{output_file_format}"
                    file_path = os.path.join(output_folder, file_name)
                    audio_segment.export(file_path, format=output_file_format)
                    logging.info(f"Audio saved to {file_path}")

                    # TODO: need to create new initialize a call detail
                    new_call_detail = CallDetail(
                        call_id=call_id,
                        audio_path=file_path,
                        # stil false
                        started_at=(elapsed_time - chunk_duration) + iteration,
                        # stil false
                        ended_at=elapsed_time + iteration,
                    )
                    uow.call_detail.create(new_call_detail)
                    uow.commit()

                    # async_process_audio(uow, file_path, new_call_detail.id)

                    response = requests.post(
                        f"http://localhost:8000/calls/{new_call_detail.id}/sentiment",
                        json={"file_path": file_path},
                    )
                    if response.status_code == 200:
                        logging.info("Sentiment analysis initiated")

                    # Increment the chunk index and reset the audio_data buffer
                    chunk_index += 1
                    audio_data = io.BytesIO()

                    # for started_at and ended_at
                    iteration += 10

        # Save any remaining audio data
        if audio_data.tell() > 0:
            audio_data.seek(0)
            audio_segment = AudioSegment.from_file(
                audio_data, format=source_file_format
            )
            file_name = f"{call_id}_{chunk_index}.{output_file_format}"
            file_path = os.path.join(output_folder, file_name)
            audio_segment.export(file_path, format=output_file_format)
            logging.info(f"Audio saved to {file_path}")

            # TODO: need to create new initialize a call detail
            new_call_detail = CallDetail(
                call_id=call_id,
                audio_path=file_path,
                # stil false
                started_at=iteration,
                # stil false
                ended_at=elapsed_time + iteration,
            )
            uow.call_detail.create(new_call_detail)
            uow.commit()

            response = requests.post(
                f"http://localhost:8000/calls/{new_call_detail.id}/sentiment",
                json={"file_path": file_path},
            )
            if response.status_code == 200:
                logging.info("Sentiment analysis initiated")

        # TODO: Combine all audio chunks into a single file
        output_file_name = f"{call_id}_combined.{output_file_format}"
        combine_audio_files(
            output_folder,
            output_file_name,
            format_output_type=output_file_format,
            format_input_type=output_file_format,
        )

        file_path = os.path.join(output_folder, output_file_name)

        # TODO: invoke upload function to upload to firestorage
        url = uow.firestorage.upload(file_path)
        logging.info(f"File uploaded to {url}")
        # remove file from the folder

        create_recording(uow, call_id, url)

        # uow.recording.create(
        #     Recording(
        #         call_id=call_id,
        #         url=url
        #     )
        # )
        # uow.commit()


def combine_audio_files(
    input_folder: str,
    output_file_name: str,
    format_output_type="wav",
    format_input_type="wav",
):
    # Create an empty AudioSegment to store the combined audio
    combined_audio = AudioSegment.empty()

    # Iterate over all files in the input folder
    for file_name in sorted(os.listdir(input_folder)):
        if file_name.endswith(f".{format_input_type}"):
            # Load each file and append it to the combined audio
            file_path = os.path.join(input_folder, file_name)
            audio_segment = AudioSegment.from_file(
                file_path, format=format_input_type
            )
            combined_audio += audio_segment

    file_path = os.path.join(input_folder, output_file_name)
    # Export the combined audio to a single file
    combined_audio.export(file_path, format=format_output_type)
    logging.info(f"Combined audio saved to {file_path}")
