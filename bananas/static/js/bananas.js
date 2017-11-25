Suit.$(function () {
    function appendClear( dateObj, dateStr, instance ) {
        const $clear = $(
            '<div class="flatpickr-clear">' +
            '<button class="btn btn-link flatpickr-clear-button">' +
            'Clear' +
            '</button>' +
            '</div>' )
            .on( 'click', () => {
                instance.clear();
                instance.close();
            } )
            .appendTo( $( instance.calendarContainer ) );
    }
    flatpickr(".datetime-input", {
        enableTime: true,
        altInput: true,
        minuteIncrement: 1,
        onReady: appendClear
    });
    flatpickr(".time-input", {
        noCalendar: true,
        enableTime: true,
        altInput: true,
        minuteIncrement: 1,
        onReady: appendClear
    });
});
