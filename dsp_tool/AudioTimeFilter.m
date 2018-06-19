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
function dsp_tool = AudioTimeFilter(waveform)
%% Reading in the audio file

clc; % clears the console
clearvars -except waveform; %Clear all variables from the workspace

if nargin == 1
    p = py.os.path.pathsep;
    waveform = [waveform char(p)];

    audioFile = erase(waveform, ":");
else if nargin == 0
    fprintf('Please enter the location of an audio file you wish to analyze:\n');

    [file, path] = uigetfile({'*.wav';}, 'Input Audio file');
    if file==0
        fprintf('\nNo file chosen. Exiting.\n');
        return
    end
    audioFile = fullfile(path, file);
    end
end

fprintf('\t%s selected\n',file);

[audioWave, sampleRate] = audioread(audioFile);
timeStep = 1/sampleRate;
%{
Above code checks the number of input arguments...
if its 0, that means AudioTimeFilter has been run locally and the user
wants to select an audio file from their filesystem

if its 1, we assume that the call has come from our python script, and a 
string has been provided from python. At this point, we need to convert the
string (python object) to a matlab char array, then uset that filepath as 
the audio file
%}

%{
read in the audio inofrmation from an audio file as provided by the user. 
Note this function reads in the audio file as a measure of the amplitude 
at a given sample rate, creating a column vector. Becuase of this, 
subsequent variables will be created in this fashion as either column 
vecotrs or matracies for consistency. Alternatively, for testing purposes,
the above can be commented out and the line below can be used
%}

%[audioWave, sampleRate] = audioread('audio\file\location\here.wav')

%% Band Seperation and Normalization

bandMatrix(1:length(audioWave),4) = 0;

bandMatrix(:,1) = bandpass(audioWave,[1815 1835],sampleRate);   %Letter
bandMatrix(:,2)  = bandpass(audioWave,[1325 1335],sampleRate);  %Space
bandMatrix(:,3) = bandpass(audioWave,[815 835],sampleRate);     %Backspace
bandMatrix(:,4) = bandpass(audioWave,[345 365],sampleRate);     %Send

%{
The above code applies 4 bandpass filters across the selected audio file.
These bands correspond to the dominant freqencies for a letter, space,
backsapce and send. Each band frequency is saved to a different column in
a matrix called bandMatrix. The columns of bandMatrix will be the
convention for the rest of the file:
    
    1: letter
    2: space 
    3: backspace 
    4: send
%}

%% Identifying Perceived Keypresses for Each Band

j = 1;
k = 1;

peakThreshold = 0.12;

for i = 1:size(bandMatrix,2)
    
    j = 1;
    
    while j <= length(audioWave)
    
        if bandMatrix(j,i) > peakThreshold
            
            %[max,idx] = findpeaks(peak);
            
            switch(i)
                
                case 1
                    keypressFound(k,1:2) = [j 1];
                    keypressWave{k,1} = bandMatrix(j:j+200,i);
                    j = j + 500;
                case 2
                    keypressFound(k,1:2) = [j 2];
                    keypressWave{k,1} = bandMatrix(j:j+200,i);
                    j = j + 500;
                case 3
                    keypressFound(k,1:2) = [j 3];
                    keypressWave{k,1} = bandMatrix(j:j+200,i);
                    j = j + 500;
                case 4
                    keypressFound(k,1:2) = [j 4];
                    keypressWave{k,1} = bandMatrix(j:j+5000,i);
                    j = j + 5000;

            end
            
            k = k + 1;
            
        else
            
            j = j+1;
            
        end
        
    end
    
end


%% Verifying Keypresses and Eliminating False Positives

j = 1;

iShouldExit = ~exist('keypressWave','var');
if iShouldExit 
   fprintf('\nNo key presses found in the provided sample. Exiting\n');
   return;
end

for i = 1:length(keypressWave)
    
    [m,loc] = max(keypressWave{i,1});
    
    switch keypressFound(i,2)
    
        case 1
            keypressWave{i,1} = bandMatrix(keypressFound(i,1)+loc-250:keypressFound(i,1)+loc+250,1);
        case 2
            keypressWave{i,1} = bandMatrix(keypressFound(i,1)+loc-250:keypressFound(i,1)+loc+250,2);
        case 3
            keypressWave{i,1} = bandMatrix(keypressFound(i,1)+loc-250:keypressFound(i,1)+loc+250,3);
        case 4
            keypressWave{i,1} = bandMatrix(keypressFound(i,1)+loc-750:keypressFound(i,1)+loc+750,4);
    
    end
    
    [amp,t] = findpeaks(keypressWave{i,1});
    %coeffMatrix(i,1:3) = polyfit(t,amp,2);
    coeffMatrix(i,1:3) = polyfit(t,amp,2);
    
    switch keypressFound(i,2) 
        case 4
            
            if coeffMatrix(i,1) < 0 && coeffMatrix(i,2) > 0.0004

                index(j,1) = keypressFound(i,1);
                type(j,1) = keypressFound(i,2);
                
                
            end
            
        otherwise 
            
            if coeffMatrix(i,1) < 0 && coeffMatrix(i,2) > 0.001

                index(j,1) = keypressFound(i,1);
                type(j,1) = keypressFound(i,2);
                j = j +1;       

            end
            
    end
    
end

%% Reordering Key Presses in Chronological Order

map = containers.Map(index,type);
validKeypresses(:,1) = map.keys;
validKeypresses(:,2) = map.values;

%% Determining word lengths and Calculating the Time Log

j = 1;

wordLengthArray(1:length(validKeypresses),1) = 0;

for i = 1:size(validKeypresses,1)
    
    switch validKeypresses{i,2}
        
        case 1
            
            wordLengthArray(j,1) = wordLengthArray(j,1)+1;
            
        case 2
            
            j = j + 1;
        case 3 
            
            switch wordLengthArray(j,1)

               case 0
                   
                   if j ~= 1  
                   
                       j = j - 1;
                  
                   end
                   
               otherwise
                   wordLengthArray(j,1) = wordLengthArray(j,1) - 1;            
            end
           
        case 4

            
    end
    
end

wordLengthArray = nonzeros(wordLengthArray);


%% Printing Output to Console

keypressTimeLog(1:length(validKeypresses),1) = 0;
j = 1;

if isempty(wordLengthArray)
    
    fprintf('\nNo words were found in the provided audio sample\n\n');
    
else
    
    startWord = 1;
    
    fprintf('\n%d words occured in the provided audio sample:\n\n',length(wordLengthArray));
    
    for i = 1:length(wordLengthArray)
        
       t1 = validKeypresses{startWord,1};
       t2 = validKeypresses{startWord+wordLengthArray(i,1)-1,1};
       
       wordTimeArray(i,1) = (t2 - t1)*timeStep;
       j = j+2;
       startWord = j;
       
       fprintf('\tword %d:\t\t%d letters\t%0.4f seconds\n', i, wordLengthArray(i,1), wordTimeArray(i,1));
       
    end
    
end

fprintf('\nTime Log:\n\n');
fprintf('\tA total of %d keypresses were found...\n', length(validKeypresses));
fprintf('\t%d were deemed unidentifiable and were ignored.\n\n', (length(keypressFound) - length(validKeypresses))); 

for i = 1:length(validKeypresses)

    fprintf('\tKeypress %d',i);

    switch validKeypresses{i,2}

        case 1, fprintf('(letter)');
        case 2, fprintf('(space)');
        case 3, fprintf('(backspace)');
        case 4, fprintf('(send)'); 
        otherwise, fprintf('(unknown)');

    end

    if i ~= length(validKeypresses)

        timeBetweenKeypresses = (validKeypresses{i+1,1}-validKeypresses{i,1})*timeStep;
        keypressTimeLog(i,1) = timeBetweenKeypresses;
        fprintf('\t\t%0.4f\n',timeBetweenKeypresses);

    else
        fprintf('\t\tEND MESSAGE\n')
    end
end

%% Saving the Output

if nargin == 1
    
    outputFile = matfile('to_language_model.mat', 'Writable', true);
    save('to_language_model.mat');
else
    fprintf('\nPlease enter a location and file name with a .txt extention to save this information to:\n');
    [file, path] = uiputfile({'*.txt'}, 'Save Output .txt File');
    if file == 0
        fprintf('\nNo file was chosen. Dumping results to console.\n');
    else
        filename = fullfile(path, file);
        fileID = fopen(filename,'wt');
        for idx = 1:length(wordLengthArray) 
            fprintf(fileID,'%d %0.4f\n',wordLengthArray(idx,1),wordTimeArray(idx,1));
        end
        fclose(fileID);
        fprintf('\nThe above information has been stored to %s\n', filename);
    end
end


%{
The above code block requests a filename from the user that will be used
to save the listed information. Using this file name as an identifier, a
new text file is created and wordLengthArray is printed to the newly
created file. Note that this file is stored to the Documents folder on the
host computer 
%}

%save('variables.mat','parsedAudio', 'plotMatrix', 'clickOccured', 'validKeypress', 'keyPressTimeLog');
save('variables.mat');
end
%{
uncommentting the above for loop and marked lines in the FFT loop will
allow hte user to see the time between clicks. This is calculated by
iterating through the clickOccured column vector and the difference between
the values at the current index and the next index is multiplied by the
timestep, calculating the time between keypresses. The time beging
fprintflayed is the time from the current key press to the next key press i.e.
    
    keypress 1(Identifier)  <timeTillKeypress2>
    keypress 2(Identifier)  <timeTillKeypress3>
    ...
    keypress 16(Idendifier)       END MESSAGE
%}