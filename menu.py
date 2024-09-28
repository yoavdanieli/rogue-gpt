import pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Helper function to render text
def render_text(text, font, color=WHITE):
    return font.render(text, True, color)

# Base class for menu elements
class MenuItem:
    def __init__(self, label, w, h, should_draw_label=True):
        # Fonts
        self.font = pygame.font.SysFont('Arial', 24)
        self.label_font = self.font
        self.small_font = pygame.font.SysFont('Arial', 16)

        self.label = label
        self.should_draw_label = should_draw_label
        self.rect = pygame.Rect(0, 0, w, h)  # Position will be set later

    def set_position(self, x, y):
        self.rect.topleft = (x, y)

    def draw_label(self, screen, font, label_x_offset=150):
        label_surface = render_text(self.label, font)
        screen.blit(label_surface, (self.rect.x - label_x_offset, self.rect.y))

    def draw(self, screen):
        raise NotImplementedError

    def handle_event(self, event):
        raise NotImplementedError

# Button class
class Button(MenuItem):
    def __init__(self, label, w, h, callback, color=BLUE):
        super().__init__(label, w, h, should_draw_label=False)
        self.callback = callback
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = render_text(self.label, self.font)
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()

# Slider class (like volume bar)
class Slider(MenuItem):
    def __init__(self, label, w, h, min_value, max_value, current_value):
        super().__init__(label, w, h)
        self.min_value = min_value
        self.max_value = max_value
        self.current_value = current_value

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)  # Background bar
        fill_width = ((self.current_value - self.min_value) / (self.max_value - self.min_value)) * self.rect.width
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y, fill_width, self.rect.height))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            relative_x = event.pos[0] - self.rect.x
            self.current_value = (relative_x / self.rect.width) * (self.max_value - self.min_value) + self.min_value

# TextBox class
class TextBox(MenuItem):
    def __init__(self, label, w, h, text='', font=None):
        super().__init__(label, w, h)
        self.text = text
        self.active = False  # To determine if the text box is focused
        self.font = font if font else self.small_font

    def draw(self, screen):
        # Draw background and border
        box_color = RED if self.active else GRAY
        pygame.draw.rect(screen, WHITE, self.rect)
        pygame.draw.rect(screen, box_color, self.rect, 2)
        
        # Handle text overflow
        text_surface = render_text(self.text, self.font, BLACK)
        text_width = text_surface.get_width()
        if text_width > self.rect.width - 10:  # Clip text if it overflows
            clipped_text = self.text[-int((self.rect.width - 10) / self.font.size('A')[0]):]
            text_surface = render_text(clipped_text, self.font, BLACK)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)  # Toggle activation
        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isprintable():
                self.text += event.unicode

# Menu class for managing the menu system
class Menu:
    def __init__(self, exit_callback=None, parent_menu_state=None, x_offset=200, y_start=100, y_spacing=80):
        self.items = []
        self.exit_callback = exit_callback
        self.parent_menu_state = parent_menu_state
        self.x_offset = x_offset
        self.y_start = y_start
        self.y_spacing = y_spacing

    def add_item(self, item):
        item.set_position(self.x_offset, self.y_start + len(self.items) * self.y_spacing)
        self.items.append(item)

    def draw(self, screen):
        screen.fill(BLACK)

        for item in self.items:
            if item.should_draw_label:
                item.draw_label(screen, item.label_font)  # Draw the label first
            item.draw(screen)  # Draw the menu item itself

    def handle_event(self, event):
        for item in self.items:
            item.handle_event(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and self.exit_callback:
            self.exit_callback()
