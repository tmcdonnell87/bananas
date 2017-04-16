Suit.$(function () {
    flatpickr(".datetime-input", {
        enableTime: true,
        altInput: true,
        minuteIncrement: 1
    });
    flatpickr(".time-input", {
        noCalendar: true,
        enableTime: true,
        altInput: true,
        minuteIncrement: 1
    });
});
