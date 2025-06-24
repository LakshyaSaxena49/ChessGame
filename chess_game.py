import pygame
import sys
import chess
import chess.engine
import time
import os

# Colors 
LIGHT_BROWN = (245, 222, 179)
DARK_BROWN = (139, 69, 19)
TIMER_FONT_COLOR = (0, 0, 0)
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER_COLOR = (150, 150, 150)
POPUP_COLOR = (220, 220, 220)
HIGHLIGHT_COLOR = (255, 255, 0, 128)  # Yellow with transparency
LEGAL_MOVE_COLOR = (0, 255, 0, 100)  # Green with transparency

# Chess piece images
PIECE_IMAGES = {
    'P': 'images/white_pawn.png', 'R': 'images/white_rook.png', 'N': 'images/white_knight.png',
    'B': 'images/white_bishop.png', 'Q': 'images/white_queen.png', 'K': 'images/white_king.png',
    'p': 'images/black_pawn.png', 'r': 'images/black_rook.png', 'n': 'images/black_knight.png',
    'b': 'images/black_bishop.png', 'q': 'images/black_queen.png', 'k': 'images/black_king.png',
}

# Path to Stockfish executable - UPDATE THIS PATH!
STOCKFISH_PATH = r"C:\stockfish-windows-x86-64-avx2\stockfish.exe"  # Update this to your Stockfish location

class ChessGame:
    def __init__(self):
        pygame.init()
        self.window_size = (1000, 800)
        self.board_size = 700
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Chess Game")
        self.clock = pygame.time.Clock()
        self.board = chess.Board()
        self.selected_square = None
        self.dragging_piece = None
        self.dragging_offset = (0, 0)
        self.game_started = False
        self.time_control = 5 * 60  # 5 minutes default
        self.white_time = self.time_control
        self.black_time = self.time_control
        self.last_time_update = None
        self.timer_font = pygame.font.Font(None, 30)
        self.game_mode = "Human vs Human"
        self.ai_engine = None
        self.setup_menu()
        self.piece_images = self.load_piece_images()  # Load actual images
        self.time_dropdown_open = False
        self.time_options = [("5+0", 5*60), ("10+0", 10*60), ("15+0", 15*60), ("30+0", 30*60)]
        self.current_time_option = 0
        self.popup_message = None
        self.popup_start_time = None
        self.game_over = False
        self.winner = None

    @property
    def grid_size(self):
        return self.board_size // 8

    def load_piece_images(self):
        """Load piece images from the images folder with fallback to text."""
        images = {}
        
        # Try to load actual images first
        for piece_char, image_path in PIECE_IMAGES.items():
            try:
                if os.path.exists(image_path):
                    image = pygame.image.load(image_path)
                    # Scale image to fit grid size
                    scaled_image = pygame.transform.scale(image, (self.grid_size, self.grid_size))
                    images[piece_char] = scaled_image
                else:
                    print(f"Image not found: {image_path}")
                    # Fall back to text representation
                    images[piece_char] = self.create_text_piece(piece_char)
            except Exception as e:
                print(f"Error loading {image_path}: {e}")
                # Fall back to text representation
                images[piece_char] = self.create_text_piece(piece_char)
        
        # If no images were loaded, create all text pieces
        if not images:
            print("No images found, using text pieces")
            return self.create_piece_images()
        
        return images
    
    def create_text_piece(self, piece_char):
        """Create a single text-based piece."""
        piece_symbols = {
            'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔',
            'p': '♟', 'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚'
        }
        
        surface = pygame.Surface((self.grid_size, self.grid_size), pygame.SRCALPHA)
        font = pygame.font.Font(None, 70)
        symbol = piece_symbols.get(piece_char, piece_char)
        
        # White pieces: white with black outline
        # Black pieces: black with white outline
        if piece_char.isupper():  # White pieces
            main_color = (255, 255, 255)
            outline_color = (0, 0, 0)
        else:  # Black pieces
            main_color = (0, 0, 0)
            outline_color = (255, 255, 255)
        
        # Draw outline (shadow effect)
        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                if dx != 0 or dy != 0:
                    outline_text = font.render(symbol, True, outline_color)
                    outline_rect = outline_text.get_rect(center=(self.grid_size//2 + dx, self.grid_size//2 + dy))
                    surface.blit(outline_text, outline_rect)
        
        # Draw main piece
        text = font.render(symbol, True, main_color)
        text_rect = text.get_rect(center=(self.grid_size//2, self.grid_size//2))
        surface.blit(text, text_rect)
        
        return surface

    def setup_menu(self):
        self.menu_width = self.window_size[0] - self.board_size
        self.start_button = pygame.Rect(self.board_size + 20, 20, 160, 40)
        self.resign_button = pygame.Rect(self.board_size + 20, 80, 160, 40)
        self.new_game_button = pygame.Rect(self.board_size + 20, 140, 160, 40)
        self.game_mode_button = pygame.Rect(self.board_size + 20, 200, 160, 40)
        self.time_control_button = pygame.Rect(self.board_size + 20, 260, 160, 40)

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
                pygame.draw.rect(self.screen, color, 
                                 (col * self.grid_size, row * self.grid_size, self.grid_size, self.grid_size))
        
        # Highlight selected square
        if self.selected_square is not None:
            col = chess.square_file(self.selected_square)
            row = 7 - chess.square_rank(self.selected_square)
            highlight_surface = pygame.Surface((self.grid_size, self.grid_size), pygame.SRCALPHA)
            highlight_surface.fill(HIGHLIGHT_COLOR)
            self.screen.blit(highlight_surface, (col * self.grid_size, row * self.grid_size))
            
            # Show legal moves
            for move in self.board.legal_moves:
                if move.from_square == self.selected_square:
                    to_col = chess.square_file(move.to_square)
                    to_row = 7 - chess.square_rank(move.to_square)
                    move_surface = pygame.Surface((self.grid_size, self.grid_size), pygame.SRCALPHA)
                    move_surface.fill(LEGAL_MOVE_COLOR)
                    self.screen.blit(move_surface, (to_col * self.grid_size, to_row * self.grid_size))

    def draw_pieces(self):
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                col, row = chess.square_file(square), 7 - chess.square_rank(square)
                piece_image = self.piece_images.get(piece.symbol())
                if piece_image:
                    self.screen.blit(piece_image, (col * self.grid_size, row * self.grid_size))

    def draw_timer(self):
        if not self.game_started:
            return
            
        # Update timers
        if self.last_time_update is not None and not self.game_over:
            elapsed = time.time() - self.last_time_update
            if self.board.turn:  # White's turn
                self.white_time = max(0, self.white_time - elapsed)
            else:  # Black's turn
                self.black_time = max(0, self.black_time - elapsed)
                
            # Check for time out
            if self.white_time <= 0:
                self.game_over = True
                self.winner = "Black wins on time!"
            elif self.black_time <= 0:
                self.game_over = True
                self.winner = "White wins on time!"
        
        self.last_time_update = time.time()
        
        # Draw white timer
        white_minutes = int(self.white_time // 60)
        white_seconds = int(self.white_time % 60)
        white_text = f"White: {white_minutes:02d}:{white_seconds:02d}"
        white_surface = self.timer_font.render(white_text, True, TIMER_FONT_COLOR)
        self.screen.blit(white_surface, (self.board_size + 20, 350))
        
        # Draw black timer
        black_minutes = int(self.black_time // 60)
        black_seconds = int(self.black_time % 60)
        black_text = f"Black: {black_minutes:02d}:{black_seconds:02d}"
        black_surface = self.timer_font.render(black_text, True, TIMER_FONT_COLOR)
        self.screen.blit(black_surface, (self.board_size + 20, 380))

    def draw_game_info(self):
        # Current turn
        turn_text = "White to move" if self.board.turn else "Black to move"
        if self.game_over:
            turn_text = self.winner if self.winner else "Game Over"
        
        turn_surface = self.timer_font.render(turn_text, True, TIMER_FONT_COLOR)
        self.screen.blit(turn_surface, (self.board_size + 20, 450))
        
        # Game status
        if self.board.is_checkmate():
            status_text = "Checkmate!"
        elif self.board.is_stalemate():
            status_text = "Stalemate!"
        elif self.board.is_check():
            status_text = "Check!"
        else:
            status_text = ""
            
        if status_text:
            status_surface = self.timer_font.render(status_text, True, (255, 0, 0))
            self.screen.blit(status_surface, (self.board_size + 20, 480))

    def render_button(self, button_rect, text, enabled=True):
        color = BUTTON_COLOR if enabled else BUTTON_HOVER_COLOR
        pygame.draw.rect(self.screen, color, button_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), button_rect, 2)
        
        font = pygame.font.Font(None, 24)
        text_surface = font.render(text, True, TIMER_FONT_COLOR)
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.cleanup()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_click(event.pos)

    def handle_click(self, pos):
        if self.start_button.collidepoint(pos):
            self.start_game()
        elif self.new_game_button.collidepoint(pos):
            self.new_game()
        elif self.resign_button.collidepoint(pos) and self.game_started:
            self.resign_game()
        elif self.game_mode_button.collidepoint(pos):
            self.toggle_game_mode()
        elif self.time_control_button.collidepoint(pos):
            self.cycle_time_control()
        elif self.game_started and pos[0] < self.board_size and not self.game_over:
            self.handle_board_click(pos)

    def handle_board_click(self, pos):
        col = pos[0] // self.grid_size
        row = 7 - (pos[1] // self.grid_size)
        square = chess.square(col, row)

        if self.selected_square is None:
            piece = self.board.piece_at(square)
            if piece and piece.color == self.board.turn:
                self.selected_square = square
        else:
            move = chess.Move(self.selected_square, square)
            
            # Handle pawn promotion
            if move in self.board.legal_moves:
                # Check if it's a pawn promotion
                piece = self.board.piece_at(self.selected_square)
                if (piece and piece.piece_type == chess.PAWN and 
                    ((piece.color and chess.square_rank(square) == 7) or 
                     (not piece.color and chess.square_rank(square) == 0))):
                    # Default to queen promotion
                    move = chess.Move(self.selected_square, square, promotion=chess.QUEEN)
                
                self.make_move(move)
            else:
                # Try to select new piece
                piece = self.board.piece_at(square)
                if piece and piece.color == self.board.turn:
                    self.selected_square = square
                else:
                    self.selected_square = None

    def make_move(self, move):
        self.board.push(move)
        self.selected_square = None
        
        # Check game end conditions
        if self.board.is_game_over():
            self.game_over = True
            if self.board.is_checkmate():
                winner = "White" if not self.board.turn else "Black"
                self.winner = f"{winner} wins by checkmate!"
            elif self.board.is_stalemate():
                self.winner = "Draw by stalemate!"
            elif self.board.is_insufficient_material():
                self.winner = "Draw by insufficient material!"
            elif self.board.is_fifty_moves():
                self.winner = "Draw by 50-move rule!"
            elif self.board.is_repetition():
                self.winner = "Draw by repetition!"
        elif self.game_mode == "Human vs AI" and not self.board.turn and not self.game_over:
            # AI's turn (black)
            pygame.time.set_timer(pygame.USEREVENT + 1, 500)  # Delay AI move slightly

    def make_ai_move(self):
        try:
            if not self.ai_engine:
                self.ai_engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
            
            result = self.ai_engine.play(self.board, chess.engine.Limit(time=1))
            self.make_move(result.move)
        except Exception as e:
            print(f"Stockfish not available, using simple AI")
            # Simple AI that prioritizes: captures > checks > random moves
            self.make_simple_ai_move()
    
    def make_simple_ai_move(self):
        """Simple AI that makes decent moves without external engine"""
        import random
        
        legal_moves = list(self.board.legal_moves)
        if not legal_moves:
            return
        
        # Prioritize moves by type
        captures = []
        checks = []
        other_moves = []
        
        for move in legal_moves:
            # Check if move is a capture
            if self.board.is_capture(move):
                captures.append(move)
            # Check if move gives check
            elif self.board.gives_check(move):
                checks.append(move)
            else:
                other_moves.append(move)
        
        # Choose move with some strategy
        if captures:
            # Prefer captures of higher value pieces
            move = random.choice(captures)
        elif checks:
            # Give check if no good captures
            move = random.choice(checks)
        else:
            # Random move otherwise
            move = random.choice(other_moves)
        
        self.make_move(move)

    def start_game(self):
        if not self.game_started:
            self.game_started = True
            self.board.reset()
            self.game_over = False
            self.winner = None
            self.white_time = self.time_options[self.current_time_option][1]
            self.black_time = self.time_options[self.current_time_option][1]
            self.last_time_update = time.time()
            print("Game started")

    def new_game(self):
        self.cleanup()
        self.game_started = False
        self.board.reset()
        self.game_over = False
        self.winner = None
        self.selected_square = None
        self.white_time = self.time_options[self.current_time_option][1]
        self.black_time = self.time_options[self.current_time_option][1]
        self.last_time_update = None
        print("New game ready")

    def resign_game(self):
        if self.game_started and not self.game_over:
            self.game_over = True
            winner = "Black" if self.board.turn else "White"
            self.winner = f"{winner} wins by resignation!"

    def toggle_game_mode(self):
        if not self.game_started:
            self.game_mode = "Human vs AI" if self.game_mode == "Human vs Human" else "Human vs Human"
            print(f"Game mode changed to: {self.game_mode}")

    def cycle_time_control(self):
        if not self.game_started:
            self.current_time_option = (self.current_time_option + 1) % len(self.time_options)

    def cleanup(self):
        if self.ai_engine:
            try:
                self.ai_engine.quit()
            except:
                pass
            self.ai_engine = None

    def run(self):
        try:
            while True:
                # Handle AI move timer
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.cleanup()
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.USEREVENT + 1:
                        pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # Cancel timer
                        if self.game_mode == "Human vs AI" and not self.board.turn and not self.game_over:
                            self.make_ai_move()
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.handle_click(event.pos)
                
                # Clear screen
                self.screen.fill((240, 240, 240))
                
                # Draw game elements
                self.draw_board()
                self.draw_pieces()
                self.draw_timer()
                self.draw_game_info()
                
                # Draw UI buttons
                self.render_button(self.start_button, "Start Game", not self.game_started)
                self.render_button(self.new_game_button, "New Game", True)
                self.render_button(self.resign_button, "Resign", self.game_started and not self.game_over)
                self.render_button(self.game_mode_button, f"Mode: {self.game_mode[:8]}", not self.game_started)
                
                time_text = f"Time: {self.time_options[self.current_time_option][0]}"
                self.render_button(self.time_control_button, time_text, not self.game_started)
                
                pygame.display.flip()
                self.clock.tick(60)
                
        except KeyboardInterrupt:
            print("\nGame interrupted by user")
        finally:
            self.cleanup()
            pygame.quit()

if __name__ == "__main__":
    game = ChessGame()
    game.run()