$('.radio__input').prop('checked', false);

document.querySelectorAll('[name=order_type]').forEach(s => {
  s.addEventListener('click', function() {
    document.querySelectorAll('.order_options').forEach(d => d.classList.add('deactive'));
    document.getElementById(this.value).classList.remove('deactive');
  });
});
