from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, Boolean, Enum, DateTime
from bookstoreapp import db, app
from sqlalchemy.orm import relationship, backref
from enum import Enum as UserEnum
from flask_login import UserMixin
from datetime import datetime

class UserRole(UserEnum):
    CASH = 1
    INVEN = 2
    ADMIN = 3

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

class Category(BaseModel):
    __tablename__ = 'category'
    name = Column(String(50), nullable=False)
    Products = relationship('Product', backref='category', lazy=True)
    def __str__(self):
        return self.name

class Product(BaseModel):
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, default=0)
    quantity = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    image = Column(String(200))
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    receipt_details = relationship("ReceiptDetails", backref='product', lazy=True)
    bookentry_details = relationship("BookEntryDetails", backref='product', lazy=True)

class Tag(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    def __str__(self):
        return self.name

prod_tag = db.Table('prod_tag',
                  Column('product_id', ForeignKey(Product.id), nullable=False, primary_key=True),
                  Column('tag_id', ForeignKey(Tag.id), nullable=False, primary_key=True))


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    avatar = Column(String(500))
    user_role = Column(Enum(UserRole), default=UserRole.CASH)
    receipts = relationship("Receipt", backref='user', lazy=True)
    bookentrys = relationship("BookEntry", backref="user", lazy=True)
    def __str__(self):
        return self.name

class Customer(BaseModel):
    name = Column(String(50), nullable=False)
    address = Column(Text)
    sdt = Column(String(50), nullable=False)
    email = Column(String(50))
    receipts = relationship('Receipt', backref='customer', lazy=True)

class Receipt(BaseModel):
    created_time = Column(DateTime, default=datetime.now())
    is_active = Column(Boolean, default=False)
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=True)
    details = relationship('ReceiptDetails', backref='receipt', lazy=True)

class ReceiptDetails(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)

class BookEntry(BaseModel):
    entry_time = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship("BookEntryDetails", backref='bookentry', lazy=True)

class BookEntryDetails(BaseModel):
    quantity = Column(Integer, default=0)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    bookentry_id = Column(Integer, ForeignKey(BookEntry.id), nullable=False)

class Rule(BaseModel):
    name = Column(String(50), nullable=True)
    value = Column(Integer, default=0)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        #
        # rl = Rule(name="Số ngày hủy hóa đơn", value=30)
        # rl2 = Rule(name="Giới hạn số lượng", value=300)
        # rl3= Rule(name="Số lượng nhập", value=150)
        # db.session.add_all([rl, rl2, rl3])
        # db.session.commit()
        #
        # import hashlib
        # password = str(hashlib.md5("1234567".encode('utf-8')).hexdigest())
        # u1 = User(name="Online", username="admin", password=password, avatar="https://i.ytimg.com/vi/Zr-qM5Vrd0g/maxresdefault.jpg", user_role=UserRole.ADMIN)
        # db.session.add(u1)
        # db.session.commit()
        #
        # c1 = Category(name="Sách")
        # c2 = Category(name="Tạp chí")
        # c3 = Category(name="Báo")
        # db.session.add_all([c1, c2, c3])
        # db.session.commit()
        #
        # p1 = Product(name="How to Win Friends & Influence People by Dale Carnegie",
        #              description="You can go after the job you want...and get it! You can take the job you have...and improve it! You can take any situation you're in...and make it work for you! Simon & Schuster Audio is proud to present one of the best-selling books of all time, Dale Carnegie's perennial classic How to Win Friends and Influence People, presented here in its entirety.",
        #              price=349000,
        #              quantity=200,
        #              image="https://m.media-amazon.com/images/P/0671027034.01._SCLZZZZZZZ_SX500_.jpg",
        #              category_id=1)
        # p2 = Product(name="Moby Dick by Herman Melville",
        #              description="Moby Dick is the story of Captain Ahab's quest to avenge the whale that 'reaped' his leg. The quest is an obsession and the novel is a diabolical study of how a man becomes a fanatic. But it is also a hymn to democracy. Bent as the crew is on Ahab s appalling crusade, it is equally the image of a co-operative community at work: all hands dependent on all hands, each individual responsible for the security of each. Among the crew is Ishmael, the novel's narrator, ordinary sailor, and extraordinary reader. Digressive, allusive, vulgar, transcendent, the story Ishmael tells is above all an education: in the practice of whaling, in the art of writing. With an Introduction and Notes by David Herd. Lecturer in English and American Literature at the University of Kent at Canterbury",
        #              price=499000,
        #              quantity=200,
        #              image="https://m.media-amazon.com/images/P/0143105957.01._SCLZZZZZZZ_SX500_.jpg",
        #              category_id=1)
        # p3 = Product(name="Catch Me If You Can by Frank W. Abagnale",
        #              description="Frank W. Abagnale, alias Frank Williams, Robert Conrad, Frank Adams, and Robert Monjo, was one of the most daring con men, forgers, imposters, and escape artists in history. In his brief but notorious criminal career, Abagnale donned a pilot's uniform and copiloted a Pan Am jet, masqueraded as the supervising resident of a hospital, practiced law without a license, passed himself off as a college sociology professor, and cashed over $2.5 million in forged checks, all before he was 21. Known by the police of 26 foreign countries and all 50 states as "'The Skywayman'", Abagnale lived a sumptuous life on the lam - until the law caught up with him.",
        #              price=549000,
        #              quantity=200,
        #              image="https://m.media-amazon.com/images/P/0767905385.01._SCLZZZZZZZ_SX500_.jpg",
        #              category_id=1)
        # p4 = Product(name="American Psycho by Bret Easton Ellis",
        #              description="Patrick Bateman moves among the young and trendy in 1980s Manhattan. Young, handsome, and well educated, Bateman earns his fortune on Wall Street by day while spending his nights in ways we cannot begin to fathom. Expressing his true self through torture and murder, Bateman prefigures an apocalyptic horror that no society could bear to confront.",
        #              price=549000,
        #              quantity=200,
        #              image="https://m.media-amazon.com/images/P/0679735771.01._SCLZZZZZZZ_SX500_.jpg",
        #              category_id=1)
        # p5 = Product(name="The Shining by Stephen King",
        #              description="Jack Torrance’s new job at the Overlook Hotel is the perfect chance for a fresh start. As the off-season caretaker at the atmospheric old hotel, he’ll have plenty of time to spend reconnecting with his family and working on his writing. But as the harsh winter weather sets in, the idyllic location feels ever more remote . . . and more sinister. And the only one to notice the strange and terrible forces gathering around the Overlook is Danny Torrance, a uniquely gifted five-year-old",
        #              price=699000,
        #              quantity=200,
        #              image="https://m.media-amazon.com/images/P/0385121679.01._SCLZZZZZZZ_SX500_.jpg",
        #              category_id=1)
        # p6 = Product(name="The Silence of the Lambs by Thomas Harris",
        #              description="A serial murderer known only by a grotesquely apt nickname―Buffalo Bill―is stalking particular women. He has a purpose, but no one can fathom it, for the bodies are discovered in different states. Clarice Starling, a young trainee at the F.B.I. Academy, is surprised to be summoned by Jack Crawford, Chief of the Bureau's Behavioral Science section. Her assignment: to interview Dr. Hannibal Lecter, a brilliant psychiatrist and grisly killer now kept under close watch in the Baltimore State Hospital for the Criminally Insane. Lecter's insight into the minds of murderers could help track and capture Buffalo Bill. Smart and attractive, Starling is shaken to find herself in a strange, intense relationship with the acutely perceptive Lecter. His cryptic clues―about Buffalo Bill and about her―launch Clarice on a search that every reader will find startling, harrowing, and totally compelling.",
        #              price=499000,
        #              quantity=200,
        #              image="https://m.media-amazon.com/images/P/0312022824.01._SCLZZZZZZZ_SX500_.jpg",
        #              category_id=1)
        # p7 = Product(name="Little Women by Louisa May Alcott",
        #              description="Grown-up Meg, tomboyish Jo, timid Beth, and precocious Amy. The four March sisters couldn't be more different. But with their father away at war, and their mother working",
        #              price=349000,
        #              quantity=200,
        #              image="https://m.media-amazon.com/images/P/0147514010.01._SCLZZZZZZZ_SX500_.jpg",
        #              category_id=1)
        # p8 = Product(name="Diary of a Wimpy Kid Book 17: Diper Överlöde by Jeff Kinney",
        #              description="When he decides to tag along with his brother Rodrick’s band, Löded Diper, Greg doesn’t realize what he’s getting into. But he soon learns that late nights, unpaid gigs, fighting between band members, and money troubles are all part of the rock ’n’ roll lifestyle. Can Greg help Löded Diper become the legends they think they are? Or will too much time with Rodrick’s band be a diper överlöde?",
        #              price=299000,
        #              quantity=200,
        #              image="https://m.media-amazon.com/images/P/141976294X.01._SCLZZZZZZZ_SX500_.jpg",
        #              category_id=1)
        # p9 = Product(name="Red Dragon by Thomas Harris",
        #              description="A quiet summer night...a neat suburban house...and another innocent, happy family is shattered - the latest victims of a grisly series of hideous sacrificial killings that no one understands, and no one can stop. Nobody lives to tell of the unimaginable carnage. Only the blood-stained walls bear witness. All hope rests on Special Agent Will Graham, who must peer inside the killer's tortured soul to understand his rage, to anticipate and prevent his next vicious crime. Desperate for help, Graham finds himself locked in a deadly alliance with the brilliant Dr. Hannibal Lecter, the infamous mass murderer who Graham put in prison years ago. As the imprisoned Lecter tightens the reins of revenge, Graham's feverish pursuit of the Red Dragon draws him inside the warped mind of a psychopath, into an unforgettable world of demonic ritual and violence, beyond the limits of human terror.",
        #              price=349000,
        #              quantity=200,
        #              image="https://m.media-amazon.com/images/I/51Edeeg8t5L._SX332_BO1,204,203,200_.jpg",
        #              category_id=1)
        # p10 = Product(name="Pride and Prejudice by Jane Austen",
        #              description="In a publishing career that spanned less than a decade, Jane Austen revolutionized the literary romance, using it as a stage from which to address issues of gender politics and class-consciousness rarely expressed in her day. The Collection included 'Sense and Sensibility', 'Pride and Prejudice', 'Mansfield Park', 'Emma', 'Northanger Abbey', 'Persuasion', and 'Lady Susan' - represent all of Austen's mature work as a novelist, and provide the reader with an introduction to the world she and her memorable characters inhabited. Also added to this beautiful collection the readers can find the Letters of Jane Austen and a Memoir made by James Edward Austen-Leigh.",
        #              price=299000,
        #              quantity=200,
        #              image="https://m.media-amazon.com/images/I/51s2Sl4NIxL.jpg",
        #               category_id=1)
        # p11 = Product(name="Vouge",
        #              description="Vogue places fashion in the context of culture and the world we live in—what we wear, how we live, who leads and inspires us. Vogue immerses itself in fashion, always leading readers to what will happen next. Thought-provoking, relevant, values driven and influential, Vogue defines the culture of fashion.",
        #              price=449000,
        #              quantity=200,
        #              image="https://m.media-amazon.com/images/I/81J6KSJIfuL._AC_SY500_.jpg",
        #               category_id=2)
        # p12 = Product(name="People",
        #              description="America's Most Popular Magazine. Defining celebrity, driving conversation and inspiring action. We're America's trusted connection to the people you want to know and the",
        #              price=799000,
        #              quantity=200,
        #              image="https://m.media-amazon.com/images/I/61fwpy9V2sL._AC_.jpg",
        #              category_id=2)
        # p13 = Product(name="The New Yorker",
        #              description="In 1925, Harold Ross established The New Yorker as a lighthearted, Manhattan-centric magazine—a “fifteen-cent comic paper,” he called it. Today, it is considered by many to",
        #              price=899000,
        #              quantity=200,
        #              image="https://m.media-amazon.com/images/I/616CE24mGYL._AC_.jpg",
        #               category_id=2)
        # p14 = Product(name="National Geographic Magazine",
        #              description="NATIONAL GEOGRAPHIC, the flagship magazine of the National Geographic Society, chronicles exploration and adventure, as well as changes that impact life on Earth. Editorial coverage encompasses people and places of the world, with an emphasis on human involvement in a changing universe. Major topics include culture, nature, geography, ecology, science and technology.",
        #              price=449000,
        #              quantity=200,
        #              image="https://m.media-amazon.com/images/I/61hCPOqI3TL._AC_.jpg",
        #               category_id=2)
        # p15 = Product(name="GQ",
        #              description="Dive into GQ’s culture-defining covers with Timothée Chalamet, Travis Scott, Zendaya, Daniel Craig, LeBron James, and more. From dynamic storytelling to elevated style—if",
        #              price=299000,
        #              quantity=200,
        #              image="https://m.media-amazon.com/images/I/61Vhbm7oMzL._AC_.jpg",
        #               category_id=2)
        # p16 = Product(name="Rolling Stone",
        #              description="Rolling Stone magazine is a cultural icon. It's the number one pop culture reference point for 13 million young adults. In addition to its authoritative position in music, Rolling",
        #              price=649000,
        #              quantity=200,
        #              image="https://m.media-amazon.com/images/I/51fw6pbNSRL._AC_.jpg",
        #               category_id=2)
        # p17 = Product(name="Elle",
        #              description="Elle is the world's largest fashion magazine edited for woman with a style - and a mind - of her own. Features include lifestyle, culture, entertainment, politics, music, theater and the arts.",
        #              price=349000,
        #              quantity=200,
        #              image="https://m.media-amazon.com/images/I/61vGpYqLlmL._AC_.jpg",
        #               category_id=2)
        # p18 = Product(name="TIME Magazine",
        #              description="TIME reveals what today's headlines mean to you and your family -- from politics, to science, to human achievement, arts, business, and society.",
        #              price=449000,
        #              quantity=200,
        #              image="https://m.media-amazon.com/images/I/61YgTrRGBtL._AC_.jpg",
        #               category_id=2)
        # p19 = Product(name="Sports Illustrated",
        #              description="Brand "'like new'" magazine, with small 3" 'crease on lower right, has never been read. Name and address have been carefully inked out on label. I wrap carefully and ship fast.'"",
        #              price=449000,
        #              quantity=200,
        #              image="https://m.media-amazon.com/images/I/51d0ev263fL._SX386_BO1,204,203,200_.jpg",
        #               category_id=2)
        # p20 = Product(name="Reader's Digest",
        #              description="Contains digest and original articles on a wide variety of health-related topics. Also contains short abstracts of current medical progress in section entitled "'News from the World of Medicine.'"",
        #              price=349000,
        #              quantity=200,
        #              image="https://m.media-amazon.com/images/I/61ff1G5KsIL._AC_.jpg",
        #               category_id=2)
        # p21 = Product(name="BÁO NHÂN DÂN",
        #              description="Kỳ xuất bản: Hàng ngày Quý III: Nghỉ 1 kỳ ngày 03/9 Các điểm in: Hà Nội, Điện Biên, Lai Châu, Nghệ An, Đà Nẵng, Đắc Lắc, Bình Định, TP.Hồ Chí Minh, Cần Thơ...",
        #              price=6000,
        #              quantity=200,
        #              image="https://bizweb.dktcdn.net/100/112/377/products/e1478b65923bfd5e4e221ec5ada2439f-copy.jpg?v=1496454999790",
        #               category_id=3)
        # p22 = Product(name="TUỔI TRẺ",
        #              description="Kỳ xuất bản: Hàng ngày",
        #              price=7000,
        #              quantity=200,
        #              image="https://bizweb.dktcdn.net/100/112/377/products/b49-tuoi-tre-tp-hcm.png?v=1586413506637",
        #               category_id=3)
        # p23 = Product(name="BÁO HOA HỌC TRÒ",
        #              description="Kỳ xuất bản: Thứ 2 cách tuần",
        #              price=35000,
        #              quantity=200,
        #              image="https://bizweb.dktcdn.net/thumb/grande/100/112/377/products/hoa-hoc-tro.jpg?v=1495763916967",
        #               category_id=3)
        # p24 = Product(name="LAO ĐỘNG",
        #              description="Kỳ xuất bản: Thứ 2, 3, 4, 5, 6, 7",
        #              price=7000,
        #              quantity=200,
        #              image="https://bizweb.dktcdn.net/100/112/377/products/bao-lao-dong.jpg?v=1495768383610",
        #               category_id=3)
        # p25 = Product(name="TIỀN PHONG",
        #              description="Kỳ xuất bản: Hàng ngày",
        #              price=7000,
        #              quantity=200,
        #              image="https://bizweb.dktcdn.net/100/112/377/products/tr1a-abdy.jpg?v=1496041912880",
        #               category_id=3)
        # p26 = Product(name="THỂ THAO VÀ VĂN HOÁ",
        #              description="Kỳ xuất bản: Thứ 2,3,4,5,6. Thị trường các tỉnh phía Bắc. Các tỉnh miền Trung và miền Nam mã N03",
        #              price=7000,
        #              quantity=200,
        #              image="https://bizweb.dktcdn.net/100/112/377/products/234.jpg?v=1496197122457",
        #               category_id=3)
        # p27 = Product(name="THANH NIÊN",
        #              description="Kỳ xuất bản: Hàng ngày.",
        #              price=7000,
        #              quantity=200,
        #              image="https://bizweb.dktcdn.net/100/112/377/products/thanh-nien.jpg?v=1496114826583",
        #               category_id=3)
        # p28 = Product(name="MỰC TÍM",
        #              description="Kỳ xuất bản: Thứ 4.",
        #              price=9000,
        #              quantity=200,
        #              image="https://bizweb.dktcdn.net/100/112/377/products/muc-tim-logo.jpg?v=1496110790667",
        #               category_id=3)
        # p29 = Product(name="BÁO BÓNG ĐÁ",
        #              description="Kỳ xuất bản: Hàng ngày",
        #              price=8000,
        #              quantity=200,
        #              image="https://bizweb.dktcdn.net/100/112/377/products/images.jpg?v=1495680076717",
        #               category_id=3)
        # p30 = Product(name="BÁO QUÂN ĐỘI NHÂN DÂN",
        #              description="Kỳ xuất bản: Hàng ngày",
        #              price=6000,
        #              quantity=200,
        #              image="https://bizweb.dktcdn.net/100/112/377/products/bao-quan-doi-nhan-dan-copy.jpg?v=1495677685553",
        #              category_id=3)
        #
        # db.session.add_all([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17, p18, p19, p20, p21, p22, p23, p24, p25, p26, p27, p28, p29, p30])
        # db.session.commit()




