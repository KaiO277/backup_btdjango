
    $(document).ready(function() {
        // Sự kiện khi người dùng chọn tệp tin
        $('#id_avatar').change(function() {
            readURL(this);
        });

        // Hàm để đọc URL của tệp tin và hiển thị ảnh trước
        function readURL(input) {
            if (input.files && input.files[0]) {
                var reader = new FileReader();

                reader.onload = function(e) {
                    // Hiển thị ảnh trước trong thẻ img
                    $('#avatar-preview').attr('src', e.target.result);
                };

                // Đọc dữ liệu từ tệp tin
                reader.readAsDataURL(input.files[0]);
            }
        }
    });

    