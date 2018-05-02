%{
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                            Audio Time Filter
                        Created by Ryan Martineau
        For ENGR5000 - Professor Aaron Carpenter, Winter 2018 

The program below takes a recording of a sequence of smartphone keyboard
clicks and isolates each peak, calculates the Fast Fourier Transform (FFT)
of each peak, and determines if either a letter or space was typed, then 
saves a sequence of numbers representing the number of letters each word 
contains to a text file as specified by the user. Backspace and send tones 
are also taken into account. Along with this information, the time it takes
for each word to be typed is also recorded. Note that the format for time 
logging the words may change.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%}
clc;% clears the console
clearvars;%Clear all variables from the workspace

fprintf('Please enter the location of an audio file you wish to analyze:\n');

[file, path] = uigetfile({'*.wav';}, 'Input Audio file');
if file==0
    fprintf('\nNo file chosen. Exiting.\n');
    return
end
audioFile = fullfile(path, file);
[audioWave, sampleRate] = audioread(audioFile);

%{
read in the audio inofrmation from an audio file as provided by the user. 
Note this function reads in the audio file as a measure of the amplitude 
at a given sample rate, creating a column vector. Becuase of this, 
subsequent variables will be created in this fashion as either column 
vecotrs or matracies for consistency. Alternatively, for testing purposes,
the above can be commented out and the line below can be used
%}

%[audioWave, sampleRate] = audioread('audio\file\location\here.wav');

idx = 1;%index that will be used to iterate through samples
jdx = 1;%index that will be used to save amplitude information 

sampleLength = 1000;%number of samples being used to calculate the FFT
timeStep = 1/sampleRate;%duration of time between samples

while idx <= length(audioWave) 
    
    if abs(audioWave(idx,1)) >= 0.135 
       
        clickOccured(jdx,1) = idx;
        click = audioWave(idx-(sampleLength/2):idx+((sampleLength/2) - 1));
        parsedAudio{jdx,1} = click;
        jdx = jdx + 1;
        idx = idx + sampleLength/2; 
        
    end   
    
    idx = idx + 1; 
    
end 

%{
The above while loop ueses idx to iterate through the audio file sample by 
sample and determines if the absolute value of the amplitude at that sample
is greater than a set threshold. If it is above this threshold, then a key 
press has occured. To capture the entire waveform of the key press, 500 
samples before and after this determined point are saved to a sperate cell 
array. The sample at which it was determined that a key press occured is 
also saved to a seprate column vector called clickOccured The iterator is 
then incremented to 500 samples after the point the key press was found. 
This porcess is repeated until idx exceeds the number of samples in the 
aduio file
%}

plotMatrix(1:sampleLength,1:length(parsedAudio)+1) = 0;
df = sampleRate/sampleLength;
frequency = -sampleRate/2:df:sampleRate/2-df;
plotMatrix(1:sampleLength,1) = frequency;

%{
The above code creates a matrix that will store the FFT of waveform for
each key press captured. This matrix will be 1000 rows long accomidating 
for the sample length used, and will have 1 column deadicated to each 
waveform, with the exception of the first column, which will contain the 
frequency range. This way, the data can be correlated without any need to 
actually graph the FFT. 
%}

jdx = 1;%Index used above must be reset because of the different context

wordLengthArray(1:length(parsedAudio),1) = 0;

%{
The above column vector is created to house the number of letters in each
word. In the subsequent for loop, each time it is determined that a
letter has occured, the value at the current index is incremented. At the
detection of a space, the pointer jdx is incremented to the next index.
Note that it's length is equal to the number of peaks that occur.
%}

startWord = 1;
endWord = 1;
messageSent = 0;

%{
The two above indexes will be used to mark the beginning and end of a word
in the column vector timeLog. MessageSent will be a flag to signal if a the
sent key has been detected. in the case where the sent key is not detected,
then a secondary procedure must be taken to ensure that the timing can be
logged properly.
%}


for idx =  1:length(parsedAudio)
    
    plotMatrix(1:sampleLength,idx+1) = abs(fftshift(fft(parsedAudio{idx,1}))/length(fft(parsedAudio{idx,1})));
    [m,n] = max(plotMatrix(:,idx+1));

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                               LETTER
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if abs(plotMatrix(n,1)) > 1700 && abs(plotMatrix(n,1)) < 1900 
        wordLengthArray(jdx,1) = wordLengthArray(jdx,1) + 1;
        endWord = endWord + 1; 
        clickOccured(idx,2) = 1;
        %^uncommenting this line will allow the user to see how much time
        % there was between keypresses

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                               SPACE
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    elseif abs(plotMatrix(n,1)) > 1200 && abs(plotMatrix(n,1)) < 1400
        endWord = endWord - 1;
        timeLog(jdx,1) = (((clickOccured(endWord,1)+499) - (clickOccured(startWord,1)-500))*timeStep);
        startWord = endWord + 2;
        endWord = startWord;
        jdx = jdx + 1;
        clickOccured(idx,2) = 2;
        %^uncommenting this line will allow the user to see how much time
        % there was between keypresses

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                             BACKSPACE
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    elseif abs(plotMatrix(n,1)) > 700 && abs(plotMatrix(n,1)) < 900

           switch wordLengthArray(jdx,1)

               case 0
                   
                   if jdx ~= 1  
                   
                       jdx = jdx - 1;
                  
                   end
                   
               otherwise
                   wordLengthArray(jdx, 1) = wordLengthArray(jdx, 1) - 1;            
           end
           
           clickOccured(idx,2) = 3;
           %^uncommenting this line will allow the user to see how much time
           % there was between keypresses

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                               SEND
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
   elseif abs(plotMatrix(n,1)) > 200  && abs(plotMatrix(n,1)) < 400
       
       timeLog(jdx,1) = (((clickOccured(endWord,1)+499)-(clickOccured(startWord,1)-500))*timeStep);
       
       parsedAudio = parsedAudio(1:idx,1);
       plotMatrix = plotMatrix(1:sampleLength,1:idx+1);
       clickOccured(idx,2) = 4;
       messageSent = 1;
       clickOccured = clickOccured(1:idx,1:2);
       %^uncommenting this line will allow the user to see how much time
       % there was between keypresses 
       break;
 
    end
    
    if idx == length(parsedAudio) && messageSent == 0
   
        endWord = endWord - 1;
        timeLog(jdx,1) = (((clickOccured(endWord,1)+499)-(clickOccured(startWord,1)-500))*timeStep);
    
    end
    
end

%{
The above for loop iterates through each cell in the parsedAudio cell
array, accessing it, and computing the FFT from the captured peak. This FFT
computation is then stored into a column in the matrix plotMatrix. The max
value of this new column is then computed, returning the max value and the
index in the matrix where it occured. Because the FFT is in the same matrix
as the frequency range, the same index where this max occcured can be used
to determine the frequency of this maximum. If the frequency is between
1700 and 1900 Hz, then the key press is a letter and the value 
wordLengthArray at the current index, represented by jdx, and the marker 
indicating the end of a word, represented by endWord, are incemented. If 
the frequency at the maximum value is between 1200 and 1400 Hz, then the 
key press is a space, and then jdx is incremented, representing the start 
of a new word. The index of endWord is moved back to the previous value in 
clickOccured. This compensates for the previous incrementation of endWord. 
The time it takes for the word to be typed is calculated and the index of 
startWord is then set to endWord, effectively resetting where the next word
begins in the clickOccured array. If the frequency at the maximum value is 
between 700 and 900 Hz, then a backspace occured. If the current index of 
the wordLengthArray is not equal to 1, this means that it is not the first
index of the array. This eliminates the possibility of throwing an error 
when a backspace occurs as the first key press. If this condition is met, 
then if the value at the current index is greater than 0, the value is 
decremented, otherwise the current index is moved to the previous value. 
Finally, if the frequency is at the maximum value is between 200 and 400 
Hz, then the key press is a send signifying the end of the message. 
In this casethe remaining peaks are removed from the parsedAudio
cell array and any excess columns from the plotMatrix are removed. The for
loop is then broken out of. If a send keypress does not occur in the
provided audio sample, then endWord must be decremneted to compnstaion for
its previous incrmenation. The time for the word to be typed is then
calculated and put into the next index in the timeLog column vector
%}

wordLengthArray = nonzeros(wordLengthArray);
%removes any zero from the column vector

fprintf(1,'\n%d words occured in the provided audio sample:\n\n', length(wordLengthArray));

for idx = 1:length(wordLengthArray)
        fprintf('\tword %d:\t\t%d letters\t%0.4f seconds\n',idx,wordLengthArray(idx,1),timeLog(idx,1));
end

%{
The above for loop iterates through wordLengthsArray and prints the word
index and how many letters there were for that index.
%}

fprintf('\nPlease enter a location and file name with a .txt extention to save this information to:\n');
[file, path] = uiputfile({'*.txt'}, 'Save Output .txt File');
if file == 0
    fprintf('\nNo file was chosen. Dumping results to console.\n');
else
    filename = fullfile(path, file);
    fileID = fopen(filename,'wt');
    for idx = 1:length(wordLengthArray) 
        fprintf(fileID,'%d %0.4f\n',wordLengthArray(idx,1),timeLog(idx,1));
    end
    fclose(fileID);
    fprintf('\nThe above information has been stored to %s\n', filename);
end

%{
The above code block requests a file name from the user that will be used
to save the listed information. Using this file name as an identifier, a
new text file is created and wordLengthArray is printed to the newly
created file. Note that this file is stored to the Documents folder on the
host computer 
%}   

fprintf('\nTime Log\n\n');
for idx = 1:length(clickOccured)
    
    fprintf('\tKeypress %d',idx);
   
    switch clickOccured(idx,2)
       
        case 1, fprintf('(letter)');
        case 2, fprintf('(space)');
        case 3, fprintf('(backspace)');
        case 4, fprintf('(send)');
        otherwise, fprintf('(unknown)');
       
    end
   
    if idx ~= length(clickOccured)
        
        timeBetweenKeypresses = (clickOccured(idx+1,1)-clickOccured(idx,1))*timeStep;
        fprintf('\t\t%0.4f\n',timeBetweenKeypresses);
        
    else
        fprintf('\t\tEND MESSAGE\n')
    end
end


%{
uncommentting the above for loop and marked lines in the FFT loop will
allow hte user to see the time between clicks. This is calculated by
iterating through the clickOccured column vector and the difference between
the values at the current index and the next index is multiplied by the
timestep, calculating the time between keypresses. The time beging
displayed is the time from the current key press to the next key press i.e.
    
    keypress 1(Identifier)  <timeTillKeypress2>
    keypress 2(Identifier)  <timeTillKeypress3>
    ...
    keypress 16(Idendifier)       END MESSAGE
%}