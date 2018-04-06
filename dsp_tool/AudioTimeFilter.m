%{
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                            Audio Time Filter
                        Created by Ryan Martineau
        For ENGR5000 - Professor Aaron Carpenter, Winter 2018 

The program below takes a recording of a sequence of smartphone keyboard
clicks and isolates each peak, calculates the Fast Fourier Transform (FFT)
of each peak, and determines if either a letter or space was typed, then 
saves a sequence of numbers representing the number of letters each word 
contains to a text file as specified by the user. Note that sends and 
backspaces are ignored now, but functionality accomidateing for these will 
be added later.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%}
clc;% clears the console
clearvars;%Clear all variables from the workspace

prompt = 'Please enter the location of an audio file you wish to analyze:\n';
audioFile = input(prompt,'s');
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
jdx = 1;%index that will be used to save information to other variables

sampleLength = 1000;%number of samples being used to calculate the FFT

while idx <= length(audioWave) 
    
    if abs(audioWave(idx,1)) >= 0.135 
        
        click = audioWave(idx-(sampleLength/2):idx+((sampleLength/2) - 1));
        parsedAudio{jdx,1} = click;
        jdx = jdx + 1;
        idx = idx + sampleLength/2;
        %startTimeAnalysis = 
        
    end    
    idx = idx + 1; 
    
end 

%{
The above while loop ueses idx to iterate through the audio file sample by 
sample and determines if the absolute value of the amplitude at that sample
is greater than a set threshold. If it is above this threshold, then a peak 
has occured. To capture the entire peak, 500 samples before and after this
determined point are saved to a sperate cell array. The iterator is then
incremented to 500 samples after the point the peak was found. This porcess
is repeated until idx exceeds the number of samples in the aduio file
%}

plotMatrix(1:sampleLength,1:length(parsedAudio)+1) = 0;
df = sampleRate/sampleLength;
frequency = -sampleRate/2:df:sampleRate/2-df;
plotMatrix(1:sampleLength,1) = frequency;

%{
The above code creates a matrix that will store the FFT of each peak
captured. This matrix will be 1000 rows long accomidating for the sample
length used, and will have 1 column deadicated to each peak, with the
exception of the first column, which will contain the frequency range. This
way, the data can be correlated without any need to actually graph the FFT. 
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

for idx =  1:length(parsedAudio)
    
    rawToFFT =abs(fftshift(fft(parsedAudio{idx,1}))/length(fft(parsedAudio{idx,1})));
    plotMatrix(1:sampleLength,idx+1) = rawToFFT;

    [m,n] = max(plotMatrix(:,idx+1));

    if abs(plotMatrix(n,1)) > 1700 && abs(plotMatrix(n,1)) < 1900 
        wordLengthArray(jdx,1) = wordLengthArray(jdx,1) + 1;

    elseif abs(plotMatrix(n,1)) > 1200 && abs(plotMatrix(n,1)) < 1400
        jdx = jdx + 1;
       
    elseif abs(plotMatrix(n,1)) > 700 && abs(plotMatrix(n,1)) < 900 

           switch wordLengthArray(jdx, 1)

               case 0
                   
                   if jdx ~= 1
                   
                       jdx = jdx - 1;
                   
                   end
                   
               otherwise
                   wordLengthArray(jdx, 1) = wordLengthArray(jdx, 1) - 1;            
           end

   elseif abs(plotMatrix(n,1)) > 200  && abs(plotMatrix(n,1)) < 400
       
       parsedAudio = parsedAudio(1:idx,1);
       plotMatrix = plotMatrix(1:sampleLength,1:idx+1);
       break;
 
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
1700 and 1900 Hz, then the peak is a letter and the value wordLengthArray 
at the current index, represented by jdx, is incemented. If the frequency 
at the maximum value is between 1200 and 1400 Hz, then the peak is a space,
and then jdx is incremented, representing the start of a new letter. If the
frequency at the maximum value is between 700 and 900 Hz, then a backspace
occured. If the current index of the wordLengthArray is not equal to 1,
this means that it is not the first index of the array. This eliminates the
possibility of throwing an error when a backspace occurs as the first peak.
If this condition is met, them if the value at the current index is greater
than 0, the value is decremented, otherwise the current index is moved to
the previous value. Finally, if the frequency is at the maximum value is
between 200 and 400 Hz, then the peak is a send signifying the end of the 
message. In this case the remaining peaks are removed from the parsedAudio
cell array and any excess columns from the plotMatrix are removed. The for
loop is then broken out of.
%}

wordLengthArray = nonzeros(wordLengthArray);
%removes any zero from the column vector 

fprintf(1,'\n%d words occured in the provided audio sample:\n\n', length(wordLengthArray));

for idx = 1:length(wordLengthArray) 
    fprintf('\tword %d:\t\t%d letters\n',idx,wordLengthArray(idx,1));
end

%{
The above for loop iterates through wordLengthsArray and prints the word
index and how many letters there were for that index. 
%}

prompt = '\nPlease enter a location and file name with a .txt extention to save this information to:\n';
filename = input(prompt,'s');
if isempty(filename) 
    fprintf('No file was chosesn\n');
else
    fileID = fopen(filename,'wt');
    fprintf(fileID,'%d\n',wordLengthArray);
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

%new comments, code, whatever