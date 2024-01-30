function redirectToAssignment(ukolId) {
    window.location.href = "{{ url_for('assignment', ukol_id='') }}".replace('', ukolId);
}