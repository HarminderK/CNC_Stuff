#include <Arduino.h>

//   A B C D E F G H
//   | | | | | | | |
//   _ _ _ _ _ _ _ _ 
//  |_|_|_|_|_|_|_|_| ----- 0
//  |_|_|_|_|_|_|_|_| ----- 1
//  |_|_|_|_|_|_|_|_| ----- 2
//  |_|_|_|_|_|_|_|_| ----- 3 
//  |_|_|_|_|_|_|_|_| ----- 4
//  |_|_|_|_|_|_|_|_| ----- 5
//  |_|_|_|_|_|_|_|_| ----- 6
//  |_|_|_|_|_|_|_|_| ----- 7
//      



// Pins for Rows: 0 - 7
int rows[] = {2, 3, 4, 5, 6, 7, 8, 9};

// Pins for Columns: A - H
String cols[] = {"10", "11", "12", "13", "A1", "A2", "A3", "A4"};

// Dimensions of the board
int num_of_cols = 8;
int num_of_rows = 8;


void initBoard(String board[8][8]) {

     board = 
     {
        {"r","n","b","q","k","b","n","r"},
        {"p","p","p","p","p","p","p","p"},
        {"","","","","","","",""},
        {"","","","","","","",""},
        {"","","","","","","",""},
        {"","","","","","","",""},
        {"P","P","P","P","P","P","P","P"},
        {"R","N","B","K","Q","B","N","R"}
     };
 }

String ownPiecePickedUpType = "";
String enemyPiecePickedUpType = "";

// Pointer to string on the board
String *positionPieceUnknown = NULL;
String *enemyPiecePickedUpPosition = NULL;

int checkMatrix(String type, String current_board[8][8], String board_difference[8][8]) {

     // Check each square for changes
     // Iterating through each row
     for(int i = 0; i < num_of_rows; i ++) {

         // Active the current row
         setRow(rows[i], HIGH);

         // Stores the value detected for each column in the row
         String row[num_of_cols];

         // Checking each column
         for(int j = 0; j < num_of_cols; j++) {
            
             // Current square status BEFORE actually checking
             String current_square = current_board[i][j];
            
             // New current square
             row[j] = checkRowColumns(cols[j]);

             // Checking possible moves
             // The piece isn't there anymore
             if(row[j] == "" && current_square != "" ) {
                 
                 if((type == "lowerCase" && current_square.islower()) || (type == "upperCase" && !current_square.islower())) {

                     // Picked up own piece. Possibly a simple move.
                     if(ownPiecePickedUpType == NULL)
                        ownPiecePickedUpType = current_square;
                     else return -1; // More than 1 own piece picked up

                 } else {
                    
                     // Enemy piece picked up. Possibly an "attack" move.
                     if(enemyPiecePickedUpType == NULL){
                        enemyPiecePickedUpType = current_square;
                        enemyPiecePickedUpPosition = &row[j];
                     }
                     else return -1; // More than 1 enemy piece picked up
                 }
                  
                 
             // A piece on square that wasn't there previously AND no other unknown piece
             } else if(row[j] != "" && current_square == "" && positionPieceUnknown == NULL) {
                  
                  // Get Pointer
                  positionPieceUnknown = &row[j];

             // TODO: Implement types of possible moves
             } else if(row[j] != "" && current_square == "" && positionPieceUnknown != NULL) {
                 return -2; // More than 1 piece (More than one piece moved/placed)
             } else {
                 return -3; // Don't know what happened...
             }
             
         }
         // Updating the row
         current_board[i] = row;

     }

     // Simple move
     if(ownPiecePickedUpType != "" && positionPieceUnknown != NULL && enemyPiecePickedUpType == "" && enemyPiecePickedUpPosition == NULL) {
        
         // Use pointer to place the piece
         *positionPieceUnknown = ownPiecePickedUpType;

         // Clear variables
         ownPiecePickedUpType = "";
         positionPieceUnknown = NULL; // Clear pointer
         
     // An "Attack" move
     } else if(ownPiecePickedUpType != "" && positionPieceUnknown == NULL && 
                 enemyPiecePickedUpType != "" && enemyPiecePickedUpPosition != NULL) {
         
         *enemyPiecePickedUpPosition = ownPiecePickedUpType;
         enemyPiecePickedUpPosition = NULL;
         ownPiecePickedUpType = "";
         enemyPiecePickedUpType = "";
     }

     return 0;
}


void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
 }

// the loop function runs over and over again forever
void loop() {
  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);                       // wait for a second
  digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
  delay(1000);                       // wait for a second
}

