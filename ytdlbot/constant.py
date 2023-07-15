#!/usr/local/bin/python3
# coding: utf-8

# ytdlbot - constant.py
# 8/16/21 16:59
#

__author__ = "Benny <benny.think@gmail.com>"

import os

from config import (
    AFD_LINK,
    COFFEE_LINK,
    ENABLE_CELERY,
    FREE_DOWNLOAD,
    REQUIRED_MEMBERSHIP,
    TOKEN_PRICE,
)
from database import InfluxDB
from utils import get_func_queue


class BotText:
    start = "مرحبا بك في بوت ألحمدي لتحميل من يوتيوب وجميع منصات التواصل ارسل رابط الفيديو. اكتب /help لمزيد من المعلومات. المطور: @MOH_ALHAMDI. استمتع😁."
    help = f"""
1. يجب أن يعمل هذا البوت في جميع الأوقات. إذا لم يعمل، فأرجو الانتظار لبضع دقائق وإعادة إرسال الرابط مرة أخرى.  

2. في وقت كتابة هذا النص، يستهلك هذا البوت أكثر من 100 جيجابايت من حركة الشبكة يوميًا.
لمنع إساءة الاستخدام، يقتصر كل مستخدم على 5 عمليات تحميل في الـ 24 ساعة.  

3. لديك خيار شراء المزيد من الرموز. اكتب /buy للمزيد من المعلومات.  

4. سيظل كود المصدر لهذا البوت مفتوحًا دائمًا ويمكن العثور عليه هنا: https://github.com/tgbot-collection/ytdlbot  

5. تحتاج مساعدة في النشر أو ميزات حصرية؟ أقدم خدمة مدفوعة - اتصل بي على @BennyThink
    """

    about = "محمل YouTube بواسطة @BennyThink.\\n\\nالمصدر المفتوح على GitHub: https://github.com/tgbot-collection/ytdlbot"

    buy = f"""
**الشروط:**
1. يمكنك استخدام هذه الخدمة مجانًا لما يصل إلى {FREE_DOWNLOAD} عمليات تحميل خلال فترة 24 ساعة، بغض النظر عما إذا كان التحميل ناجحًا أم لا.  

2. يمكنك شراء رموز تحميل إضافية، والتي ستكون صالحة إلى أجل غير مسمى.   

3. لن أجمع أي معلومات شخصية، لذلك لن أعرف كم أو أي مقاطع فيديو قمت بتنزيلها.  

4. الاسترجاعات ممكنة، ولكن ستكون مسؤولاً عن رسوم المعالجة التي يفرضها مزود الدفع (Stripe ، Buy Me a Coffee ، إلخ).

5. سأسجل معرفك الفريد بعد دفع ناجح ، وهو عادة معرّف الدفع الخاص بك أو عنوان البريد الإلكتروني.  

6. يمكن للمستخدم المدفوع تغيير وضع التنزيل الافتراضي إلى الوضع المحلي في الإعدادات، والذي أسرع. إذا استنفدت جميع رموزك ، سيتم إعادة تعيينك إلى الوضع الافتراضي.

**سعر رمز التحميل:**
1. الجميع: {FREE_DOWNLOAD} رموز لكل 24 ساعة، مجانًا.  
2. 1 USD == {TOKEN_PRICE} رموز، صالحة إلى أجل غير مسمى.
3. 7 CNY == {TOKEN_PRICE} رموز، صالحة إلى أجل غير مسمى.  

**خيار الدفع:**  
1. AFDIAN (AliPay، WeChat Pay وPayPal): {AFD_LINK}  
2. اشتر لي قهوة: {COFFEE_LINK}
3. دفع Telegram (Stripe)، انظر الفاتورة التالية.   

**بعد الدفع:**

1. Afdian: قدِّم رقم طلب الشراء مع الأمر /redeem (مثال: `/redeem 123456`).
2. اشتر لي قهوة: قدم بريدك الإلكتروني مع الأمر /redeem (مثال: `/redeem some@one.com`). **استخدم بريدًا إلكترونيًا مختلفًا في كل مرة.**  
3. دفع Telegram: سيتم تفعيل دفعتك تلقائيًا.

تريد شراء المزيد من الرموز في وقت واحد؟ دعنا نقول 100؟ تفضل! `/buy 123`
    """
    private = "هذا البوت للاستخدام الخاص"
    membership_require = f"تحتاج إلى الانضمام إلى هذه المجموعة أو القناة لاستخدام هذا البوت\\n\\nhttps://t.me/{REQUIRED_MEMBERSHIP}"

    settings = """
يرجى اختيار التنسيق وجودة الفيديو المرغوبة.ملاحظة أن هذه الإعدادات تنطبق فقط على مقاطع الفيديو من YouTube.

يوصى بالجودة العالية. الجودة المتوسطة هي 720P ، في حين أن الجودة المنخفضة هي 480P.

يرجى مراعاة أنه إذا اخترت إرسال الفيديو كمستند ، فلن يكون من الممكن بثه.

إعداداتك الحالية:
جودة الفيديو: **{0}**
تنسيق الإرسال: **{1}**
"""
    custom_text = os.getenv("CUSTOM_TEXT", "")

    @staticmethod
    def get_receive_link_text() -> str:
        reserved = get_func_queue("reserved")
        if ENABLE_CELERY and reserved:
            text = f"Too many tasks. Your tasks was added to the reserved queue {reserved}."
        else:
            text = "Your task was added to active queue.\nProcessing...\n\n"

        return text

    @staticmethod
    def ping_worker() -> str:
        from tasks import app as celery_app

        workers = InfluxDB().extract_dashboard_data()
        # [{'celery@BennyのMBP': 'abc'}, {'celery@BennyのMBP': 'abc'}]
        response = celery_app.control.broadcast("ping_revision", reply=True)
        revision = {}
        for item in response:
            revision.update(item)

        text = ""
        for worker in workers:
            fields = worker["fields"]
            hostname = worker["tags"]["hostname"]
            status = {True: "✅"}.get(fields["status"], "❌")
            active = fields["active"]
            load = "{},{},{}".format(fields["load1"], fields["load5"], fields["load15"])
            rev = revision.get(hostname, "")
            text += f"{status}{hostname} **{active}** {load} {rev}\n"

        return text
