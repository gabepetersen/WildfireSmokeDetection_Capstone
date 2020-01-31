/*
File Name: main.cpp
Application: FrameExtractor
Author(s): William Williams
Version:
	- 1.0 : Complete Program January 30, 2020
Purpose:
	- Extract a set number of frames from each video in a folder
		and save those frames as a new video in a seperate folder.
*/


#include <opencv2/opencv.hpp> // Video processing functionality
#include <direct.h>			// Windows directory functionallity
#include <iostream>			// std::cout and std::cin for debugging purposes
#include <string>			// String functionality
#include <filesystem>		// Interact with directives and files
#include <functional>		// Used for hash function
#include <windows.h>		// Change directory functionality
#include <fstream>			// Input/Output file functionality

using namespace cv;
namespace fs = std::filesystem;

// Function Prototypes
long getNumberFramesManual(const std::string);
long getNumberFramesAutomatic(const std::string);
std::string getVideoNameHash(const std::string);
void selectFrames(int, long, const std::string, const std::string);
void getVideoNames(std::vector<std::string>*);
void saveHashedNames(const std::vector<std::string>*, std::string);

/*
Function Name: main()
Author: William Williams
Date: January 28, 2020
Arguments:
Return:
	-int : 0 is the default return value.
Purpose:
	- Entry point of the program. Perform operation...
			- Sets up folders for processed videos.
			- Calls function to retrieve the video file names
			- Calls function to get frame count of each video
			- Calls function to select frames from each video
				and create a new video with these frames.
			- Moves new video into folder of processed videos.
			- Saves hashed processed video names to a text file.
*/
int main(int argv, char* argc)
{
	// Vector Data Structure to hold all video file names.
	std::vector<std::string> videoFileNames;
	// Vector Data Structure to hold hashed video file names.
	std::vector<std::string> hashVideoFileNames;
	// Variable to hold number of frames in each video.
	long numberFrames = 0;

	// Setup the directory to save the processed videos into.
	fs::path saveVideosPath = fs::current_path();
	std::string saveVideosDirectory = saveVideosPath.string() + "\\ProcessedVideos";

	// If the folder already exists, it and everything in it.
	if (fs::exists("ProcessedVideos"))
	{
		fs::remove_all("ProcessedVideos");
	}

	// Create a new folder for the processed videos.
	fs::create_directory("ProcessedVideos");

	// Ensure that a folder exists for holding the WildFireVideos.
	if (!fs::exists("WildFireVideos"))
	{
		fs::create_directory("WildFireVideos");
	}

	// Call function to retrieve and store all of the video names.
	getVideoNames(&videoFileNames);

	// Change the working directory to the WildFireVideos Folder.
	// This is neccessary because OpenCV only works on items in 
	// the current working directory.
	std::wstring videoDirectory = L"\WildFireVideos";
	LPCWSTR videoDirectoryLPCWSTR = videoDirectory.c_str();
	SetCurrentDirectoryW(videoDirectoryLPCWSTR);

	// Loop through all of the videos.
	for (int i = 0; i < videoFileNames.size(); i++)
	{
		// Get number of frames from metadata.
		numberFrames = getNumberFramesAutomatic(videoFileNames.at(i));

		// If automatic frame count fails, do it manually.
		if (numberFrames <= 0)
		{
			getNumberFramesManual(videoFileNames.at(i));
		}

		// Get the processed video name. This will be the hash of the original
		// video with the extension '.avi'.
		std::string newVideoName = getVideoNameHash(videoFileNames.at(i));
		hashVideoFileNames.push_back(newVideoName);

		// Call the select frames function which will pull out the number
		// specified frames and create a new video of them.
		selectFrames(5, numberFrames, videoFileNames.at(i), newVideoName);

		// This string specifies the desired location and name for the processed
		// video to be saved.
		std::string newFileLocation = saveVideosDirectory + "\\" + newVideoName;

		// Move the processed video to the ProcessedVideos folder and remove
		// the video from the current directory.
		fs::copy_file(newVideoName, newFileLocation);
		fs::remove(newVideoName);
	}

	// Save hashed video names into text file
	saveHashedNames(&hashVideoFileNames, saveVideosDirectory);

	return 0;
}

/*
Function Name: getNumberFramesAutomatic()
Author: William Williams
Date: January 28, 2020
Arguments:
	-const std::string videoName : video name and location
Return:
	-long : The number of frames in the specified video.
Purpose:
	- Returns the number of frames in a video based on the 
		meta data.
*/
long getNumberFramesAutomatic(const std::string videoName)
{
	long numberFrames = 0;

	// Open the video file utilizing opencv.
	VideoCapture originalVideo(videoName);

	// Check to make sure that the specified video file has opened.
	if (!originalVideo.isOpened())
	{
		// If the video does not exist, print error message.
		std::cout << std::endl;
		std::cout << "The video file " + videoName + " does not exist." << std::endl;
		std::cout << std::endl;

		// This will cause the program to end.
		return -1;
	}
	else
	{
		// If the video does exist, call the get function with Frame Count enumerator.
		numberFrames = originalVideo.get(CAP_PROP_FRAME_COUNT);

		// Release the video capture object.
		originalVideo.release();
	}

	// Return the number of frames in the video.
	return numberFrames;
}

/*
Function Name: getNumberFramesManual()
Author: William Williams
Date: January 28, 2020
Arguments:
	-const std::string videoName : video name and location
Return:
	-long : The number of frames in the specified video.
Purpose:
	- Returns the number of frames in a video based on 
		manually incrementing frames of the video.
*/
long getNumberFramesManual(const std::string videoName)
{
	long numberFrames = 0;

	// Open the video file utilizing opencv.
	VideoCapture originalVideo(videoName);

	// Check to make sure that the specified video file has opened.
	if (!originalVideo.isOpened())
	{
		// If the video does not exist, print error message.
		std::cout << std::endl;
		std::cout << "The video file " + videoName + " does not exist." << std::endl;
		std::cout << std::endl;

		// This will cause the program to end.
		return -1;
	}
	else
	{
		// If the video does exist...
		// Create a Matrix to hold a video frame.
		Mat singleFrame;

		// Infinite While Loop
		while (true)
		{
			// Increment the number of frames when the program increments through the video
			numberFrames++;
			// Get the next frame from the video file.
			originalVideo >> singleFrame;

			// Check to see if the frame is empty
			if (singleFrame.empty())
			{
				// If the frame is empty,
				// it means we reached the end
				// of the video, so break out of loop.
				break;
			}
		}

		// Release the video object
		originalVideo.release();
	}
	
	// Return the total number of frames.
	return numberFrames;
}

/*
Function Name: getVideoNameHash()
Author: William Williams
Date: January 30, 2020
Arguments:
	-const std::string videoName : original video name.
Return:
	-std::string : Hashed original video name with '.avi' extension.
Purpose:
	- Returns the formatted name of the processed video file.
*/
std::string getVideoNameHash(const std::string name)
{
	std::size_t videoHashed;
	const std::string videoExtension = ".avi";
	std::string processedVideoName;

	videoHashed = std::hash<std::string>{}(name);

	processedVideoName = std::to_string(videoHashed) + videoExtension;

	return processedVideoName;
}

/*
Function Name: selectFrames()
Author: William Williams
Date: January 30, 2020
Arguments:
	-int numFramesSelect : number of frames to select form the video.
	-int totalNumFrames : total number of frames in the video.
	-const std::string originalFileName : original video name.
	-const std::string newFileName : hashed video name.
Return:
	-void 
Purpose:
	- Creates a new video with the desired number of frames from the original
		video. The selector will not select the first frame and will not select
		a frame close to the end of the video. It will select frames at a constant interval apart
		based on the formula frameInterval = totalFrames / (numberFramesSelect + 1).
*/
void selectFrames(int numFramesSelect, long totalNumFrames, const std::string originalFileName, const std::string newFileName)
{
	// Video Capture Object opens the original unprocessed video.
	VideoCapture originalVideo(originalFileName);

	// Check to make sure the video has opened.
	if (!originalVideo.isOpened())
	{
		// If the video does not exist, print error message.
		std::cout << std::endl;
		std::cout << "The video file " + originalFileName + " does not exist." << std::endl;
		std::cout << std::endl;

		return;
	}

	// Get frame width and height from the meta data of the original video.
	int frame_width = originalVideo.get(CAP_PROP_FRAME_WIDTH);
	int frame_height = originalVideo.get(CAP_PROP_FRAME_HEIGHT);

	// Create output video object with arguments in the following order...
	// to be created video file name
	// Video code
	// Frames per second
	// Frame Size
	VideoWriter outputVideo(newFileName, VideoWriter::fourcc('M', 'J', 'P', 'G'), 1, Size(frame_width, frame_height));
	
	// Calculate number of frames in each section.
	long frameInterval = totalNumFrames / (numFramesSelect + 1);

	// Set where to get first frame from.
	long currentFrame = frameInterval;
	originalVideo.set(CAP_PROP_POS_FRAMES, currentFrame);

	// Matrix to hold selecte frame in.
	Mat selectedFrame;

	// Loop to get selected number of frames.
	for(int i = 0; i < numFramesSelect; i++)
	{
		if (currentFrame <= totalNumFrames)
		{
			// Get frame from the original video and put it into holder matrix.
			originalVideo >> selectedFrame;

			// If the frame is empty, break immediately
			if (selectedFrame.empty())
			{
				break;
			}

			// Put the frame into the output video file.
			outputVideo.write(selectedFrame);

			// Increment the position to get the next frame from.
			currentFrame += frameInterval;
			originalVideo.set(CAP_PROP_POS_FRAMES, currentFrame);
		}
	}

	// Release both video capture and write objects.
	originalVideo.release();
	outputVideo.release();
}

/*
Function Name: getVideoNames()
Author: William Williams
Date: January 30, 2020
Arguments:
	-std::vector<std::string>* holder : Vector of strings of the video file names.
Return:
	-void
Purpose:
	- Iterates through the WildFireVideo folder and gathers all of the video file names.
*/
void getVideoNames(std::vector<std::string>* holder)
{
	// Temporary string to hold file name.
	std::string fileNameHolder;

	// Use filesystem class to iterate through everyhting in the WildFireVideo folder.
	for (auto& file : fs::directory_iterator("\WildFireVideos"))
	{
		// Get just the filename and push it into the vector.
		fileNameHolder = file.path().filename().string();
		holder->push_back(fileNameHolder);
	}
}

/*
Function Name: saveHashedNames()
Author: William Williams
Date: January 30, 2020
Arguments:
	-std::vector<std::string>* hashNames : Vector of strings of the hashed video file names.
	-std::string directory : The directory to save the text file to.
Return:
	-void
Purpose:
	- Iterates through the hashed names vector and saves them to a text file.
*/
void saveHashedNames(const std::vector<std::string>* hashNames, std::string directory)
{
	// Prepare string with the directory and name of text file to save hash names to.
	const std::string fileName = directory + "\\HashedVideoNames.txt";
	std::ofstream outputSaveFile;

	// Open the file for output.
	outputSaveFile.open(fileName);

	// Check to make sure the file is open.
	if (outputSaveFile.is_open())
	{
		// Loop through the vector and save values to text file.
		for (int i = 0; i < hashNames->size(); i++)
		{
			outputSaveFile << hashNames->at(i);

			// Don't put a next line character after the last entry.
			if (i != (hashNames->size() - 1))
			{
				outputSaveFile << "\n";
			}
		}

		// Close the output file.
		outputSaveFile.close();
	}
}
