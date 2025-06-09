#Đầu bài:
#Triển khai game Tic-Tac-Toe (Chapter 6) với giao diện tkinter: bảng 3×3 và thông báo kết quả.
#Đầu vào – đầu ra:
#•	Đầu vào: Click vào ô vuông (Button).
#•	Đầu ra: X hoặc O hiện lên, hiển thị người thắng hoặc hoà.
#Tính năng yêu cầu:
#•	Theo dõi turn, legal_moves, winner.
#•	Reset game.
#•	Tắt nút sau khi click.
#Kiểm tra & kết quả mẫu:
#•	Dàn xếp thắng hàng ngang → Hiển thị “X thắng!”
#Các bước triển khai:
#1.	Class TTTBoard chứa logic.
#2.	Tạo 9 nút Button trên grid.
#3.	Gắn event click: gọi make_move(), cập nhật text nút.
#4.	Kiểm tra thắng/thua sau mỗi nước.

import tkinter as tk  # Thư viện giao diện đồ họa tkinter

# Lớp đại diện cho bảng cờ
class TTTBoard:
    def __init__(self):
        # Khởi tạo bảng 3x3 dưới dạng 1 danh sách 9 phần tử rỗng
        self.board = [''] * 9
        self.current_player = 'X'  # Người chơi bắt đầu là X
        self.winner = None  # Chưa có người thắng
        self.winning_combination = None  # Vị trí các ô thắng

    # Xử lý khi người chơi đánh vào một ô
    def make_move(self, index):
        if self.board[index] == '' and self.winner is None:
            # Đánh vào ô nếu chưa có ai đánh và chưa có người thắng
            self.board[index] = self.current_player
            if self.check_winner():
                self.winner = self.current_player  # Nếu thắng, lưu lại người thắng
            elif '' not in self.board:
                self.winner = 'Hòa'  # Nếu hết ô và chưa ai thắng → hòa
            else:
                # Chuyển lượt chơi
                self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    # Kiểm tra điều kiện thắng
    def check_winner(self):
        b = self.board
        # Các tổ hợp thắng: 3 hàng ngang, 3 cột dọc, 2 đường chéo
        wins = [
            (0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)
        ]
        for i, j, k in wins:
            if b[i] == b[j] == b[k] != '':
                self.winning_combination = (i, j, k)  # Lưu lại ô thắng để tô màu
                return True
        return False

    # Reset bảng cờ cho ván mới
    def reset(self):
        self.__init__()


# Lớp giao diện chính của ứng dụng
class TTTApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cờ Caro 3x3")
        self.board = TTTBoard()  # Tạo đối tượng bảng cờ

        self.buttons = []  # Danh sách các nút tương ứng với các ô
        for i in range(9):
            # Tạo nút cho từng ô cờ
            btn = tk.Button(root, text='', font=('Arial', 32), width=5, height=2,
                            command=lambda i=i: self.on_click(i))
            btn.grid(row=i//3, column=i%3)  # Đặt nút vào lưới 3x3
            self.buttons.append(btn)

        # Nhãn trạng thái (hiển thị lượt chơi, kết quả...)
        self.status_label = tk.Label(root, text="Lượt của người chơi X", font=('Arial', 14))
        self.status_label.grid(row=3, column=0, columnspan=3)

        # Nút chơi lại
        self.reset_button = tk.Button(root, text="Chơi lại", font=('Arial', 14),
                                      command=self.reset_game)
        self.reset_button.grid(row=4, column=0, columnspan=3, sticky='nsew')

    # Xử lý khi người chơi nhấn vào 1 ô
    def on_click(self, index):
        if self.board.make_move(index):
            # Cập nhật giao diện của ô đó
            self.buttons[index]['text'] = self.board.board[index]
            self.buttons[index]['state'] = 'disabled'
            if self.board.winner:
                self.end_game()  # Nếu có kết quả thì kết thúc ván
            else:
                # Cập nhật trạng thái hiển thị lượt tiếp theo
                self.status_label['text'] = f"Lượt của người chơi {self.board.current_player}"

    # Kết thúc ván: hiển thị kết quả và tô sáng ô thắng (nếu có)
    def end_game(self):
        for btn in self.buttons:
            btn['state'] = 'disabled'  # Khóa toàn bộ nút

        if self.board.winner == 'Hòa':
            self.status_label['text'] = "Trận đấu hòa!"
        else:
            # Tô màu các ô thắng
            i, j, k = self.board.winning_combination
            for idx in (i, j, k):
                self.buttons[idx]['bg'] = 'lightgreen'
            self.status_label['text'] = f"Người chơi {self.board.winner} thắng!"

    # Reset trò chơi
    def reset_game(self):
        self.board.reset()  # Xóa bảng cũ
        for btn in self.buttons:
            btn['text'] = ''
            btn['state'] = 'normal'
            btn['bg'] = 'SystemButtonFace'  # Khôi phục màu nền mặc định
        self.status_label['text'] = "Lượt của người chơi X"  # Reset trạng thái


# Điểm bắt đầu chương trình
if __name__ == "__main__":
    root = tk.Tk()  # Tạo cửa sổ chính
    app = TTTApp(root)  # Tạo ứng dụng
    root.mainloop()  # Vòng lặp chạy giao diện
