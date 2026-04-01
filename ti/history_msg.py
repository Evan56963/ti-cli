from dataclasses import dataclass


@dataclass
class HistoryMsg:
    uuid: str
    msgGUID: str
    isReal: bool
    importance: str  # '0' = Normal, '1' = Important, '2' = Critical
    isUse: str       # '1' = Active, '3' = Inactive, else = Preview
    isRead: bool

    @property
    def msg_type(self) -> str:
        return 'Real' if self.isReal else 'UnReal'

    @property
    def importance_label(self) -> str:
        if self.importance == '0':
            return 'Normal'
        elif self.importance == '2':
            return 'Critical'
        return 'Important'

    @property
    def is_use_label(self) -> str:
        if self.isUse == '1':
            return 'Active'
        elif self.isUse == '3':
            return 'Inactive'
        return 'Preview'

    @property
    def status_label(self) -> str:
        return 'Read' if self.isRead else 'UnRead'


class HistoryMsgList:
    PAGE_SIZE = 10

    def __init__(self):
        self._messages: list[HistoryMsg] = []
        self._current_page: int = 1

    def add(self, msg: HistoryMsg) -> None:
        self._messages.append(msg)

    def clear(self) -> None:
        self._messages.clear()
        self._current_page = 1

    @property
    def total_count(self) -> int:
        return len(self._messages)

    @property
    def total_pages(self) -> int:
        if not self._messages:
            return 1
        return (len(self._messages) + self.PAGE_SIZE - 1) // self.PAGE_SIZE

    @property
    def current_page(self) -> int:
        return self._current_page

    def go_to_first(self) -> None:
        self._current_page = 1

    def go_to_last(self) -> None:
        self._current_page = self.total_pages

    def go_to_prev(self) -> None:
        if self._current_page > 1:
            self._current_page -= 1

    def go_to_next(self) -> None:
        if self._current_page < self.total_pages:
            self._current_page += 1

    def set_page(self, page: int) -> None:
        self._current_page = max(1, min(page, self.total_pages))

    def get_current_page_messages(self) -> list[HistoryMsg]:
        start = (self._current_page - 1) * self.PAGE_SIZE
        end = start + self.PAGE_SIZE
        return self._messages[start:end]
