# Chess Game 🏁

A chess game implementation built as part of my 3rd year mini project.

## 📋 Features

- **Full Graphical Chess Interface**: Beautiful pygame-based chess board with brown wood theme
- **Dual Game Modes**: 
  - Human vs Human (local multiplayer)
  - Human vs AI (Stockfish engine)
- **Smart AI Opponent**: 
  - Primary: Stockfish engine integration with 1-second thinking time
  - Fallback: Built-in strategic AI (prioritizes captures, checks, tactical moves)
- **Interactive Gameplay**: 
  - Click-to-select and click-to-move interface
  - Visual highlight for selected pieces (yellow overlay)
  - Legal move indicators (green overlay)
- **Complete Chess Rules Implementation**:
  - All standard chess piece movements
  - Automatic pawn promotion (defaults to Queen)
  - Castling, en passant, and special moves
  - Check, checkmate, and stalemate detection
- **Game Timer System**:
  - Multiple time controls: 5+0, 10+0, 15+0, 30+0 minutes
  - Real-time countdown for both players
  - Time-based win conditions
- **Flexible Piece Graphics**:
  - Supports custom piece images (PNG format)
  - Automatic fallback to Unicode chess symbols with outlines
  - Auto-scaling to board size
- **Game Management**:
  - Start/New Game functionality
  - Resignation option
  - Game state tracking (turn indicator, check warnings)
  - Multiple end-game conditions (checkmate, stalemate, time, resignation)
- **Professional UI**:
  - Clean button interface
  - Real-time game status display
  - 60 FPS smooth gameplay

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- Stockfish chess engine
- Required Python libraries:
  - `pygame` (for graphics and game interface)
  - `python-chess` (chess library for game logic)
  - `stockfish` or `python-chess[engine]` (for chess engine integration)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/LakshyaSaxena49/ChessGame.git
   ```

2. Navigate to the project directory:
   ```bash
   cd ChessGame
   ```

3. **Set up Stockfish engine path**:
   - Download Stockfish from [official website](https://stockfishchess.org/download/)
   - Extract to your preferred location (e.g., `C:\stockfish-windows-x86-64-avx2\`)
   - Update the `STOCKFISH_PATH` variable in `chess_game.py`:
   ```python
   STOCKFISH_PATH = r"C:\your-path-to-stockfish\stockfish.exe"  # Windows
   STOCKFISH_PATH = "/usr/local/bin/stockfish"  # Linux/Mac
   ```

4. **Set up piece images (optional)**:
   - Create an `images/` folder in your project directory
   - Add PNG files for chess pieces following this naming convention:
     - `white_pawn.png`, `white_rook.png`, `white_knight.png`, etc.
     - `black_pawn.png`, `black_rook.png`, `black_knight.png`, etc.
   - If images aren't found, the game automatically uses Unicode chess symbols

5. Install required Python packages:
   ```bash
   pip install pygame
   pip install python-chess
   pip install python-chess[engine]
   ```
   
   Or install all at once:
   ```bash
   pip install pygame python-chess python-chess[engine]
   ```

### Running the Game

```bash
python chess_game.py
```

Or if you prefer to run with unbuffered output:
```bash
python -u chess_game.py
```

## 🎮 How to Play

1. **Starting the Game**: 
   - Run the application to open the pygame window
   - Choose game mode: "Human vs Human" or "Human vs AI"
   - Select time control (5, 10, 15, or 30 minutes)
   - Click "Start Game"

2. **Making Moves**: 
   - Click on a piece to select it (highlighted in yellow)
   - Click on destination square to move
   - Valid moves are shown with green highlights
   - Turn indicator shows whose move it is

3. **Game Modes**:
   - **Human vs Human**: Two players take turns on same computer
   - **Human vs AI**: Play against Stockfish engine (you play as White)

4. **Special Features**:
   - **Timer**: Counts down for each player, game ends if time runs out
   - **Resignation**: Click "Resign" to forfeit the game
   - **New Game**: Reset board and start fresh
   - **Automatic Pawn Promotion**: Pawns automatically promote to Queen

5. **Game Controls**: 
   - All interactions via mouse clicks
   - Close window to exit game

## 🏗️ Project Structure

```
ChessGame/
├── chess_game.py          # Main game file
├── assets/                # Images, sounds, or other assets (if any)
├── docs/                  # Documentation
├── tests/                 # Test files (if any)
├── requirements.txt       # Python dependencies (if any)
└── README.md             # Project documentation
```

## 🛠️ Built With

- **Python 3.x** - Core implementation
- **Pygame** - Graphics, user interface, and game loop
- **python-chess** - Chess game logic, move validation, and board representation
- **Stockfish Engine** - AI opponent and position analysis
- **Standard Python Libraries** - System operations and file handling (sys, time, os)

## 🎯 Technical Implementation

**Architecture & Design:**
- **MVC Pattern**: Clean separation of game logic, UI rendering, and user input
- **Object-Oriented Design**: Single `ChessGame` class managing all game state
- **Event-Driven Programming**: Pygame event loop with proper event handling

**Core Components:**
- **Game Engine**: python-chess library for chess logic, move validation, and game rules
- **Graphics Rendering**: Pygame for 2D board, pieces, UI elements, and animations
- **AI Integration**: 
  - Primary: Stockfish engine via python-chess engine interface
  - Fallback: Custom strategic AI with move prioritization (captures > checks > random)
- **Timer System**: Real-time countdown with automatic game termination
- **Visual Feedback**: Transparent overlays for piece selection and legal moves

**Key Technical Features:**
- **Robust Error Handling**: Graceful fallbacks for missing Stockfish or images
- **Resource Management**: Automatic cleanup of engine processes
- **Scalable UI**: Dynamic sizing based on board dimensions
- **Performance Optimized**: 60 FPS rendering with efficient event handling
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🧪 Testing

```bash
# Example
python -m pytest tests/
```

## 🚧 Future Enhancements

- [ ] **Enhanced AI Features**:
  - [ ] Adjustable Stockfish difficulty levels
  - [ ] Engine depth configuration
  - [ ] Move analysis and evaluation display
- [ ] **Advanced UI**:
  - [ ] Drag-and-drop piece movement
  - [ ] Move history display panel
  - [ ] Interactive pawn promotion dialog
  - [ ] Sound effects for moves and captures
- [ ] **Game Features**:
  - [ ] Save/Load games in PGN format
  - [ ] Undo/Redo moves
  - [ ] Opening book integration
  - [ ] Position setup from FEN
- [ ] **Multiplayer & Modes**:
  - [ ] Online multiplayer support
  - [ ] Tournament mode
  - [ ] Engine vs Engine matches
  - [ ] Puzzle/Training mode
- [ ] **Customization**:
  - [ ] Multiple board themes
  - [ ] Custom piece sets
  - [ ] Configurable time controls with increment

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Lakshya Saxena**
- GitHub: [@LakshyaSaxena49](https://github.com/LakshyaSaxena49)
- Email: [lakshyasaxena49@gmail.com]

## 🙏 Acknowledgments

- Thanks to my professors and classmates for guidance
- Chess.com for rule references
- Stockfish for AI implementation

## 📞 Support

If you encounter any issues or have questions, please feel free to:
- Open an issue on GitHub
- Contact me via email

---

⭐ If you found this project helpful, please give it a star!
