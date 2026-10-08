import streamlit as st
import anthropic
import base64

st.set_page_config(page_title="استخراج أرقام المرضى", page_icon="🆔")

st.title("🆔 استخراج أرقام المرضى")
st.write("رفع صورة التقرير لاستخراج رقم المريض (10 أرقام) فوراً")

api_key = st.text_input("أدخل مفتاح Anthropic API:", type="password")
uploaded_file = st.file_uploader("اختر صورة التقرير...", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file and api_key:
    st.image(uploaded_file, caption="الصورة المرفوعة", use_column_width=True)
    
    if st.button("استخراج رقم المريض"):
        with st.spinner("جاري تحليل الصورة بواسطة Claude..."):
            try:
                bytes_data = uploaded_file.getvalue()
                base64_image = base64.b64encode(bytes_data).decode('utf-8')
                media_type = uploaded_file.type

                client = anthropic.Anthropic(api_key=api_key)
                
                response = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=300,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image",
                                    "source": {
                                        "type": "base64",
                                        "media_type": media_type,
                                        "data": base64_image,
                                    },
                                },
                                {
                                    "type": "text",
                                    "text": "Extract only the 10-digit patient ID / Medical Record Number (MRN) from this image. Return ONLY the 10 digits without any extra text or explanation."
                                }
                            ],
                        }
                    ],
                )
                
                result = response.content[0].text.strip()
                st.success(f"تم استخراج الرقم بنجاح: **{result}**")
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء المعالجة: {e}")
