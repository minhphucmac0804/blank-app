import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import io
import base64

st.title("2. Xoay Ảnh Trực Tiếp Bằng Chuột (Nâng cao)")
st.write("Sử dụng `streamlit-drawable-canvas`")
st.info("Hướng dẫn: Chọn công cụ 'transform' (biểu tượng mũi tên 4 chiều), sau đó click vào ảnh. Một tay cầm xoay sẽ xuất hiện ở phía trên khung ảnh.")


def pil_to_base64(img):
    """Hàm chuyển đổi ảnh PIL sang chuỗi base64 để hiển thị trên canvas."""
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return "data:image/png;base64," + img_str


uploaded_file = st.file_uploader(
    "Tải ảnh lên để xoay trực tiếp",
    type=['png', 'jpg', 'jpeg'],
    key="canvas_uploader"
)

if uploaded_file is not None:
    img = Image.open(uploaded_file)

    # Giảm kích thước ảnh nếu quá lớn để canvas hoạt động tốt hơn
    img.thumbnail((600, 600))

    # Chuyển ảnh thành định dạng phù hợp để đưa vào canvas
    img_b64 = pil_to_base64(img)

    # Đặt ảnh làm đối tượng ban đầu trên canvas
    initial_drawing = {
        "version": "5.3.0",
        "objects": [
            {
                "type": "image",
                "version": "5.3.0",
                "originX": "left",
                "originY": "top",
                "left": 50, "top": 50,
                "width": img.width, "height": img.height,
                "src": img_b64,
                # "angle" có thể được set ban đầu tại đây
            }
        ],
    }

    # Tạo canvas
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=2,
        stroke_color="#000000",
        background_color="#EEEEEE",
        # Không dùng background_image, mà dùng initial_drawing
        height=500,
        width=700,
        drawing_mode="transform",  # BẬT CHẾ ĐỘ QUAN TRỌNG NHẤT
        initial_drawing=initial_drawing,
        key="full_canvas",
    )

    # Hiển thị dữ liệu khi có tương tác
    if canvas_result.json_data is not None and canvas_result.json_data["objects"]:
        st.subheader("Thông số của đối tượng ảnh:")
        # Lấy thông tin của đối tượng đầu tiên (là bức ảnh của chúng ta)
        object_info = canvas_result.json_data["objects"][0]
        st.json(object_info)
        st.write(f"**Góc xoay hiện tại:** {object_info.get('angle', 0):.2f}°")
