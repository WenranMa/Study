# Spring
## IoC容器
### IoC原理
Spring提供的容器又称为IoC容器，IoC全称Inversion of Control，直译为控制反转。在理解IoC之前，我们先看看通常的Java组件是如何协作的。

我们假定一个在线书店，通过BookService获取书籍：
```java
public class BookService {
    private HikariConfig config = new HikariConfig();
    private DataSource dataSource = new HikariDataSource(config);

    public Book getBook(long bookId) {
        try (Connection conn = dataSource.getConnection()) {
            ...
            return book;
        }
    }
}
```
为了从数据库查询书籍，BookService持有一个DataSource。为了实例化一个HikariDataSource，又不得不实例化一个HikariConfig。

现在，我们继续编写UserService获取用户：
```java
public class UserService {
    private HikariConfig config = new HikariConfig();
    private DataSource dataSource = new HikariDataSource(config);

    public User getUser(long userId) {
        try (Connection conn = dataSource.getConnection()) {
            ...
            return user;
        }
    }
}
```
因为UserService也需要访问数据库，因此，我们不得不也实例化一个HikariDataSource。

在处理用户购买的CartServlet中，我们需要实例化UserService和BookService：
```java
public class CartServlet extends HttpServlet {
    private BookService bookService = new BookService();
    private UserService userService = new UserService();

    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        long currentUserId = getFromCookie(req);
        User currentUser = userService.getUser(currentUserId);
        Book book = bookService.getBook(req.getParameter("bookId"));
        cartService.addToCart(currentUser, book);
        ...
    }
}
```
类似的，在购买历史HistoryServlet中，也需要实例化UserService和BookService：
```java
public class HistoryServlet extends HttpServlet {
    private BookService bookService = new BookService();
    private UserService userService = new UserService();
}
```
上述每个组件都采用了一种简单的通过new创建实例并持有的方式。仔细观察，会发现以下缺点：

- 实例化一个组件其实很难，例如，BookService和UserService要创建HikariDataSource，实际上需要读取配置，才能先实例化HikariConfig，再实例化HikariDataSource。
- 没有必要让BookService和UserService分别创建DataSource实例，完全可以共享同一个DataSource，但谁负责创建DataSource，谁负责获取其他组件已经创建的DataSource，不好处理。类似的，CartServlet和HistoryServlet也应当共享BookService实例和UserService实例，但也不好处理。
- 很多组件需要销毁以便释放资源，例如DataSource，但如果该组件被多个组件共享，如何确保它的使用方都已经全部被销毁？
- 随着更多的组件被引入，例如，书籍评论，需要共享的组件写起来会更困难，这些组件的依赖关系会越来越复杂。
- 测试某个组件，例如BookService，是复杂的，因为必须要在真实的数据库环境下执行。

从上面的例子可以看出，如果一个系统有大量的组件，其生命周期和相互之间的依赖关系如果由组件自身来维护，不但大大增加了系统的复杂度，而且会导致组件之间极为紧密的耦合，继而给测试和维护带来了极大的困难。

因此，核心问题是：

- 谁负责创建组件？
- 谁负责根据依赖关系组装组件？
- 销毁时，如何按依赖顺序正确销毁？

解决这一问题的核心方案就是IoC。

传统的应用程序中，控制权在程序本身，程序的控制流程完全由开发者控制，例如：

CartServlet创建了BookService，在创建BookService的过程中，又创建了DataSource组件。这种模式的缺点是，一个组件如果要使用另一个组件，必须先知道如何正确地创建它。

在IoC模式下，控制权发生了反转，即从应用程序转移到了IoC容器，所有组件不再由应用程序自己创建和配置，而是由IoC容器负责，这样，应用程序只需要直接使用已经创建好并且配置好的组件。为了能让组件在IoC容器中被“装配”出来，需要某种“注入”机制，例如，BookService自己并不会创建DataSource，而是等待外部通过setDataSource()方法来注入一个DataSource：
```java
public class BookService {
    private DataSource dataSource;

    public void setDataSource(DataSource dataSource) {
        this.dataSource = dataSource;
    }
}
```
不直接new一个DataSource，而是注入一个DataSource，这个小小的改动虽然简单，却带来了一系列好处：

BookService不再关心如何创建DataSource，因此，不必编写读取数据库配置之类的代码；
DataSource实例被注入到BookService，同样也可以注入到UserService，因此，共享一个组件非常简单；
测试BookService更容易，因为注入的是DataSource，可以使用内存数据库，而不是真实的MySQL配置。
因此，IoC又称为__依赖注入__（__Dependency Injection__），它解决了一个最主要的问题：将组件的创建+配置与组件的使用相分离，并且，由IoC容器负责管理组件的生命周期。

因为IoC容器要负责实例化所有的组件，因此，有必要告诉容器如何创建组件，以及各组件的依赖关系。一种最简单的配置是通过XML文件来实现，例如：
```xml
<beans>
    <bean id="dataSource" class="HikariDataSource" />
    <bean id="bookService" class="BookService">
        <property name="dataSource" ref="dataSource" />
    </bean>
    <bean id="userService" class="UserService">
        <property name="dataSource" ref="dataSource" />
    </bean>
</beans>
```
上述XML配置文件指示IoC容器创建3个JavaBean组件，并把id为dataSource的组件通过属性dataSource（即调用setDataSource()方法）注入到另外两个组件中。

在Spring的IoC容器中，我们把所有组件统称为__JavaBean__，即配置一个组件就是配置一个__Bean__。

#### 依赖注入方式
我们从上面的代码可以看到，依赖注入可以通过set()方法实现。但依赖注入也可以通过构造方法实现。

很多Java类都具有带参数的构造方法，如果我们把BookService改造为通过构造方法注入，那么实现代码如下：
```java
public class BookService {
    private DataSource dataSource;

    public BookService(DataSource dataSource) {
        this.dataSource = dataSource;
    }
}
```
Spring的IoC容器同时支持属性注入和构造方法注入，并允许混合使用。

#### 无侵入容器
在设计上，Spring的IoC容器是一个高度可扩展的无侵入容器。所谓无侵入，是指应用程序的组件无需实现Spring的特定接口，或者说，组件根本不知道自己在Spring的容器中运行。这种无侵入的设计有以下好处：

- 应用程序组件既可以在Spring的IoC容器中运行，也可以自己编写代码自行组装配置；
- 测试的时候并不依赖Spring容器，可单独进行测试，大大提高了开发效率。


### 装配Bean
我们前面讨论了为什么要使用Spring的IoC容器，因为让容器来为我们创建并装配Bean能获得很大的好处，那么到底如何使用IoC容器？装配好的Bean又如何使用？

我们来看一个具体的用户注册登录的例子。整个工程的结构如下：
```
spring-ioc-appcontext
├── pom.xml
└── src
    └── main
        ├── java
        │   └── com
        │       └── itranswarp
        │           └── learnjava
        │               ├── Main.java
        │               └── service
        │                   ├── MailService.java
        │                   ├── User.java
        │                   └── UserService.java
        └── resources
            └── application.xml
```

首先，我们用Maven创建工程并引入spring-context依赖：
```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.itranswarp.learnjava</groupId>
    <artifactId>spring-ioc-appcontext</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>jar</packaging>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
        <java.version>11</java.version>

        <spring.version>5.2.3.RELEASE</spring.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-context</artifactId>
            <version>${spring.version}</version>
        </dependency>
    </dependencies>
</project>
```

我们先编写一个MailService，用于在用户登录和注册成功后发送邮件通知：
```java
public class MailService {
    private ZoneId zoneId = ZoneId.systemDefault();

    public void setZoneId(ZoneId zoneId) {
        this.zoneId = zoneId;
    }

    public String getTime() {
        return ZonedDateTime.now(this.zoneId).format(DateTimeFormatter.ISO_ZONED_DATE_TIME);
    }

    public void sendLoginMail(User user) {
        System.err.println(String.format("Hi, %s! You are logged in at %s", user.getName(), getTime()));
    }

    public void sendRegistrationMail(User user) {
        System.err.println(String.format("Welcome, %s!", user.getName()));

    }
}
```

再编写一个UserService，实现用户注册和登录：
```java
public class UserService {
    private MailService mailService;

    public void setMailService(MailService mailService) {
        this.mailService = mailService;
    }

    private List<User> users = new ArrayList<>(List.of( // users:
            new User(1, "bob@example.com", "password", "Bob"), // bob
            new User(2, "alice@example.com", "password", "Alice"), // alice
            new User(3, "tom@example.com", "password", "Tom"))); // tom

    public User login(String email, String password) {
        for (User user : users) {
            if (user.getEmail().equalsIgnoreCase(email) && user.getPassword().equals(password)) {
                mailService.sendLoginMail(user);
                return user;
            }
        }
        throw new RuntimeException("login failed.");
    }

    public User getUser(long id) {
        return this.users.stream().filter(user -> user.getId() == id).findFirst().orElseThrow();
    }

    public User register(String email, String password, String name) {
        users.forEach((user) -> {
            if (user.getEmail().equalsIgnoreCase(email)) {
                throw new RuntimeException("email exist.");
            }
        });
        User user = new User(users.stream().mapToLong(u -> u.getId()).max().getAsLong() + 1, email, password, name);
        users.add(user);
        mailService.sendRegistrationMail(user);
        return user;
    }
}
```

注意到UserService通过setMailService()注入了一个MailService。

然后，我们需要编写一个特定的application.xml配置文件，告诉Spring的IoC容器应该如何创建并组装Bean：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.springframework.org/schema/beans
        https://www.springframework.org/schema/beans/spring-beans.xsd">

    <bean id="userService" class="com.itranswarp.learnjava.service.UserService">
        <property name="mailService" ref="mailService" />
    </bean>

    <bean id="mailService" class="com.itranswarp.learnjava.service.MailService" />
</beans>
```

注意观察上述配置文件，其中与XML Schema相关的部分格式是固定的，我们只关注两个<bean ...>的配置：

- 每个<bean ...>都有一个id标识，相当于Bean的唯一ID；
- 在userServiceBean中，通过<property name="..." ref="..." />注入了另一个Bean；
- Bean的顺序不重要，Spring根据依赖关系会自动正确初始化。

把上述XML配置文件用Java代码写出来，就像这样：
```java
UserService userService = new UserService();
MailService mailService = new MailService();
userService.setMailService(mailService);
```
只不过Spring容器是通过读取XML文件后使用反射完成的。

如果注入的不是Bean，而是boolean、int、String这样的数据类型，则通过value注入，例如，创建一个HikariDataSource：
```xml
<bean id="dataSource" class="com.zaxxer.hikari.HikariDataSource">
    <property name="jdbcUrl" value="jdbc:mysql://localhost:3306/test" />
    <property name="username" value="root" />
    <property name="password" value="password" />
    <property name="maximumPoolSize" value="10" />
    <property name="autoCommit" value="true" />
</bean>
```

最后一步，我们需要创建一个Spring的IoC容器实例，然后加载配置文件，让Spring容器为我们创建并装配好配置文件中指定的所有Bean，这只需要一行代码：
```java
ApplicationContext context = new ClassPathXmlApplicationContext("application.xml");
```
接下来，我们就可以从Spring容器中“取出”装配好的Bean然后使用它：
```java
// 获取Bean:
UserService userService = context.getBean(UserService.class);
// 正常调用:
User user = userService.login("bob@example.com", "password");
```

完整的main()方法如下：
```java
public class Main {
    public static void main(String[] args) {
        ApplicationContext context = new ClassPathXmlApplicationContext("application.xml");
        UserService userService = context.getBean(UserService.class);
        User user = userService.login("bob@example.com", "password");
        System.out.println(user.getName());
    }
}
```

#### ApplicationContext
我们从创建Spring容器的代码：
```java
ApplicationContext context = new ClassPathXmlApplicationContext("application.xml");
```
可以看到，Spring容器就是ApplicationContext，它是一个接口，有很多实现类，这里我们选择ClassPathXmlApplicationContext，表示它会自动从classpath中查找指定的XML配置文件。

获得了ApplicationContext的实例，就获得了IoC容器的引用。从ApplicationContext中我们可以根据Bean的ID获取Bean，但更多的时候我们根据Bean的类型获取Bean的引用：
```java
UserService userService = context.getBean(UserService.class);
```

Spring还提供另一种IoC容器叫BeanFactory，使用方式和ApplicationContext类似：
```java
BeanFactory factory = new XmlBeanFactory(new ClassPathResource("application.xml"));
MailService mailService = factory.getBean(MailService.class);
```
BeanFactory和ApplicationContext的区别在于，BeanFactory的实现是按需创建，即第一次获取Bean时才创建这个Bean，而ApplicationContext会一次性创建所有的Bean。实际上，ApplicationContext接口是从BeanFactory接口继承而来的，并且，ApplicationContext提供了一些额外的功能，包括国际化支持、事件和通知机制等。通常情况下，我们总是使用ApplicationContext，很少会考虑使用BeanFactory。


### 使用Annotation配置
使用Spring的IoC容器，实际上就是通过类似XML这样的配置文件，把我们自己的Bean的依赖关系描述出来，然后让容器来创建并装配Bean。一旦容器初始化完毕，我们就直接从容器中获取Bean使用它们。

使用XML配置的优点是所有的Bean都能一目了然地列出来，并通过配置注入能直观地看到每个Bean的依赖。它的缺点是写起来非常繁琐，每增加一个组件，就必须把新的Bean配置到XML中。

我们可以使用Annotation配置，可以完全不需要XML，让Spring自动扫描Bean并组装它们。

我们把上一节的示例改造一下，先删除XML配置文件，然后给UserService和MailService添加几个注解。

首先，我们给MailService添加一个@Component注解：
```java
@Component
public class MailService {
    ...
}
```
这个@Component注解就相当于定义了一个Bean，它有一个可选的名称，默认是mailService，即小写开头的类名。

然后，我们给UserService添加一个@Component注解和一个@Autowired注解：
```java
@Component
public class UserService {
    @Autowired
    MailService mailService;

    ...
}
```
使用@Autowired就相当于把指定类型的Bean注入到指定的字段中。和XML配置相比，@Autowired大幅简化了注入，因为它不但可以写在set()方法上，还可以直接写在字段上，甚至可以写在构造方法中：
```java
@Component
public class UserService {
    MailService mailService;

    public UserService(@Autowired MailService mailService) {
        this.mailService = mailService;
    }
    ...
}
```
我们一般把@Autowired写在字段上，通常使用package权限的字段，便于测试。

最后，编写一个AppConfig类启动容器：
```java
@Configuration
@ComponentScan
public class AppConfig {
    public static void main(String[] args) {
        ApplicationContext context = new AnnotationConfigApplicationContext(AppConfig.class);
        UserService userService = context.getBean(UserService.class);
        User user = userService.login("bob@example.com", "password");
        System.out.println(user.getName());
    }
}
```
除了main()方法外，AppConfig标注了@Configuration，表示它是一个配置类，因为我们创建ApplicationContext时：
```java
ApplicationContext context = new AnnotationConfigApplicationContext(AppConfig.class);
```
使用的实现类是AnnotationConfigApplicationContext，必须传入一个标注了@Configuration的类名。

此外，AppConfig还标注了@ComponentScan，它告诉容器，自动搜索当前类所在的包以及子包，把所有标注为@Component的Bean自动创建出来，并根据@Autowired进行装配。

整个工程结构如下：
```
spring-ioc-annoconfig
├── pom.xml
└── src
    └── main
        └── java
            └── com
                └── itranswarp
                    └── learnjava
                        ├── AppConfig.java
                        └── service
                            ├── MailService.java
                            ├── User.java
                            └── UserService.java
```
使用Annotation配合自动扫描能大幅简化Spring的配置，我们只需要保证：

- 每个Bean被标注为@Component并正确使用@Autowired注入；
- 配置类被标注为@Configuration和@ComponentScan；
- 所有Bean均在指定包以及子包内。

使用@ComponentScan非常方便，但是，我们也要特别注意包的层次结构。通常来说，启动配置AppConfig位于自定义的顶层包（例如com.itranswarp.learnjava），其他Bean按类别放入子包。


### 定制Bean
#### Scope
对于Spring容器来说，当我们把一个Bean标记为@Component后，它就会自动为我们创建一个单例（Singleton），即容器初始化时创建Bean，容器关闭前销毁Bean。在容器运行期间，我们调用getBean(Class)获取到的Bean总是同一个实例。

还有一种Bean，我们每次调用getBean(Class)，容器都返回一个新的实例，这种Bean称为Prototype（原型），它的生命周期显然和Singleton不同。声明一个Prototype的Bean时，需要添加一个额外的@Scope注解：
```java
@Component
@Scope(ConfigurableBeanFactory.SCOPE_PROTOTYPE) // @Scope("prototype")
public class MailSession {
    ...
}
```

#### 注入List
有些时候，我们会有一系列接口相同，不同实现类的Bean。例如，注册用户时，我们要对email、password和name这3个变量进行验证。为了便于扩展，我们先定义验证接口：
```java
public interface Validator {
    void validate(String email, String password, String name);
}
```
然后，分别使用3个Validator对用户参数进行验证：
```java
@Component
public class EmailValidator implements Validator {
    public void validate(String email, String password, String name) {
        if (!email.matches("^[a-z0-9]+\\@[a-z0-9]+\\.[a-z]{2,10}$")) {
            throw new IllegalArgumentException("invalid email: " + email);
        }
    }
}

@Component
public class PasswordValidator implements Validator {
    public void validate(String email, String password, String name) {
        if (!password.matches("^.{6,20}$")) {
            throw new IllegalArgumentException("invalid password");
        }
    }
}

@Component
public class NameValidator implements Validator {
    public void validate(String email, String password, String name) {
        if (name == null || name.isBlank() || name.length() > 20) {
            throw new IllegalArgumentException("invalid name: " + name);
        }
    }
}
```
最后，我们通过一个Validators作为入口进行验证：
```java
@Component
public class Validators {
    @Autowired
    List<Validator> validators;

    public void validate(String email, String password, String name) {
        for (var validator : this.validators) {
            validator.validate(email, password, name);
        }
    }
}
```
注意到Validators被注入了一个List<Validator>，Spring会自动把所有类型为Validator的Bean装配为一个List注入进来，这样一来，我们每新增一个Validator类型，就自动被Spring装配到Validators中了，非常方便。

因为Spring是通过扫描classpath获取到所有的Bean，而List是有序的，要指定List中Bean的顺序，可以加上@Order注解：
```java
@Component
@Order(1)
public class EmailValidator implements Validator {
    ...
}

@Component
@Order(2)
public class PasswordValidator implements Validator {
    ...
}

@Component
@Order(3)
public class NameValidator implements Validator {
    ...
}
```

#### 可选注入
默认情况下，当我们标记了一个@Autowired后，Spring如果没有找到对应类型的Bean，它会抛出NoSuchBeanDefinitionException异常。

可以给@Autowired增加一个required = false的参数：
```java
@Component
public class MailService {
    @Autowired(required = false)
    ZoneId zoneId = ZoneId.systemDefault();
    ...
}
```
这个参数告诉Spring容器，如果找到一个类型为ZoneId的Bean，就注入，如果找不到，就忽略。这种方式非常适合有定义就使用定义，没有就使用默认值的情况。

#### 创建第三方Bean
如果一个Bean不在我们自己的package管理之内，例如ZoneId，如何创建它？答案是我们自己在@Configuration类中编写一个Java方法创建并返回它，注意给方法标记一个@Bean注解：
```java
@Configuration
@ComponentScan
public class AppConfig {
    // 创建一个Bean:
    @Bean
    ZoneId createZoneId() {
        return ZoneId.of("Z");
    }
}
```
Spring对标记为@Bean的方法只调用一次，因此返回的Bean仍然是单例。

#### 初始化和销毁
有些时候，一个Bean在注入必要的依赖后，需要进行初始化（监听消息等）。在容器关闭时，有时候还需要清理资源（关闭连接池等）。我们通常会定义一个init()方法进行初始化，定义一个shutdown()方法进行清理，然后，引入JSR-250定义的Annotation：
```xml
<dependency>
    <groupId>javax.annotation</groupId>
    <artifactId>javax.annotation-api</artifactId>
    <version>1.3.2</version>
</dependency>
```
在Bean的初始化和清理方法上标记@PostConstruct和@PreDestroy：
```java
@Component
public class MailService {
    @Autowired(required = false)
    ZoneId zoneId = ZoneId.systemDefault();

    @PostConstruct
    public void init() {
        System.out.println("Init mail service with zoneId = " + this.zoneId);
    }

    @PreDestroy
    public void shutdown() {
        System.out.println("Shutdown mail service");
    }
}
```
Spring容器会对上述Bean做如下初始化流程：

- 调用构造方法创建MailService实例；
- 根据@Autowired进行注入；
- 调用标记有@PostConstruct的init()方法进行初始化。

而销毁时，容器会首先调用标记有@PreDestroy的shutdown()方法。

Spring只根据Annotation查找无参数方法，对方法名不作要求。

#### 使用别名
默认情况下，对一种类型的Bean，容器只创建一个实例。但有些时候，我们需要对一种类型的Bean创建多个实例。例如，同时连接多个数据库，就必须创建多个DataSource实例。

如果我们在@Configuration类中创建了多个同类型的Bean：
```java
@Configuration
@ComponentScan
public class AppConfig {
    @Bean
    ZoneId createZoneOfZ() {
        return ZoneId.of("Z");
    }

    @Bean
    ZoneId createZoneOfUTC8() {
        return ZoneId.of("UTC+08:00");
    }
}
```
Spring会报NoUniqueBeanDefinitionException异常，意思是出现了重复的Bean定义。

这个时候，需要给每个Bean添加不同的名字：
```java
@Configuration
@ComponentScan
public class AppConfig {
    @Bean("z")
    ZoneId createZoneOfZ() {
        return ZoneId.of("Z");
    }

    @Bean
    @Qualifier("utc8")
    ZoneId createZoneOfUTC8() {
        return ZoneId.of("UTC+08:00");
    }
}
```
可以用@Bean("name")指定别名，也可以用@Bean+@Qualifier("name")指定别名。

存在多个同类型的Bean时，注入ZoneId又会报错：

NoUniqueBeanDefinitionException: No qualifying bean of type 'java.time.ZoneId' available: expected single matching bean but found 2
意思是期待找到唯一的ZoneId类型Bean，但是找到两。因此，注入时，要指定Bean的名称：
```java
@Component
public class MailService {
    @Autowired(required = false)
    @Qualifier("z") // 指定注入名称为"z"的ZoneId
    ZoneId zoneId = ZoneId.systemDefault();
    ...
}
```
还有一种方法是把其中某个Bean指定为@Primary：
```java
@Configuration
@ComponentScan
public class AppConfig {
    @Bean
    @Primary // 指定为主要Bean
    @Qualifier("z")
    ZoneId createZoneOfZ() {
        return ZoneId.of("Z");
    }

    @Bean
    @Qualifier("utc8")
    ZoneId createZoneOfUTC8() {
        return ZoneId.of("UTC+08:00");
    }
}
```
这样，在注入时，如果没有指出Bean的名字，Spring会注入标记有@Primary的Bean。这种方式也很常用。例如，对于主从两个数据源，通常将主数据源定义为@Primary：
```java
@Configuration
@ComponentScan
public class AppConfig {
    @Bean
    @Primary
    DataSource createMasterDataSource() {
        ...
    }

    @Bean
    @Qualifier("slave")
    DataSource createSlaveDataSource() {
        ...
    }
}
```
其他Bean默认注入的就是主数据源。如果要注入从数据源，那么只需要指定名称即可。

#### 使用FactoryBean
我们在设计模式的工厂方法中讲到，很多时候，可以通过工厂模式创建对象。Spring也提供了工厂模式，允许定义一个工厂，然后由工厂创建真正的Bean。

用工厂模式创建Bean需要实现FactoryBean接口。我们观察下面的代码：
```java
@Component
public class ZoneIdFactoryBean implements FactoryBean<ZoneId> {

    String zone = "Z";

    @Override
    public ZoneId getObject() throws Exception {
        return ZoneId.of(zone);
    }

    @Override
    public Class<?> getObjectType() {
        return ZoneId.class;
    }
}
```
当一个Bean实现了FactoryBean接口后，Spring会先实例化这个工厂，然后调用getObject()创建真正的Bean。getObjectType()可以指定创建的Bean的类型，因为指定类型不一定与实际类型一致，可以是接口或抽象类。

因此，如果定义了一个FactoryBean，要注意Spring创建的Bean实际上是这个FactoryBean的getObject()方法返回的Bean。为了和普通Bean区分，我们通常都以XxxFactoryBean命名。

### 使用Resource
在Java程序中，我们经常会读取配置文件、资源文件等。使用Spring容器时，我们也可以把“文件”注入进来，方便程序读取。

例如，AppService需要读取logo.txt这个文件，通常情况下，我们需要写很多繁琐的代码，主要是为了定位文件，打开InputStream。

Spring提供了一个org.springframework.core.io.Resource（注意不是javax.annotation.Resource），它可以像String、int一样使用@Value注入：
```java
@Component
public class AppService {
    @Value("classpath:/logo.txt")
    private Resource resource;

    private String logo;

    @PostConstruct
    public void init() throws IOException {
        try (var reader = new BufferedReader(
                new InputStreamReader(resource.getInputStream(), StandardCharsets.UTF_8))) {
            this.logo = reader.lines().collect(Collectors.joining("\n"));
        }
    }
}
```
注入Resource最常用的方式是通过classpath，即类似classpath:/logo.txt表示在classpath中搜索logo.txt文件，然后，我们直接调用Resource.getInputStream()就可以获取到输入流，避免了自己搜索文件的代码。

也可以直接指定文件的路径，例如：
```java
@Value("file:/path/to/logo.txt")
private Resource resource;
```
但使用classpath是最简单的方式。上述工程结构如下：
```
spring-ioc-resource
├── pom.xml
└── src
    └── main
        ├── java
        │   └── com
        │       └── itranswarp
        │           └── learnjava
        │               ├── AppConfig.java
        │               └── AppService.java
        └── resources
            └── logo.txt
```
使用Maven的标准目录结构，所有资源文件放入src/main/resources即可。

### 注入配置
在开发应用程序时，经常需要读取配置文件。最常用的配置方法是以key=value的形式写在.properties文件中。

例如，MailService根据配置的app.zone=Asia/Shanghai来决定使用哪个时区。要读取配置文件，我们可以使用上一节讲到的Resource来读取位于classpath下的一个app.properties文件。但是，这样仍然比较繁琐。

Spring容器还提供了一个更简单的@PropertySource来自动读取配置文件。我们只需要在@Configuration配置类上再添加一个注解：
```java
@Configuration
@ComponentScan
@PropertySource("app.properties") // 表示读取classpath的app.properties
public class AppConfig {
    @Value("${app.zone:Z}")
    String zoneId;

    @Bean
    ZoneId createZoneId() {
        return ZoneId.of(zoneId);
    }
}
```
Spring容器看到@PropertySource("app.properties")注解后，自动读取这个配置文件，然后，我们使用@Value正常注入：
```java
@Value("${app.zone:Z}")
String zoneId;
```
注意注入的字符串语法，它的格式如下：

- "${app.zone}"表示读取key为app.zone的value，如果key不存在，启动将报错；
- "${app.zone:Z}"表示读取key为app.zone的value，但如果key不存在，就使用默认值Z。

这样一来，我们就可以根据app.zone的配置来创建ZoneId。

还可以把注入的注解写到方法参数中：
```java
@Bean
ZoneId createZoneId(@Value("${app.zone:Z}") String zoneId) {
    return ZoneId.of(zoneId);
}
```
可见，先使用@PropertySource读取配置文件，然后通过@Value以${key:defaultValue}的形式注入，可以极大地简化读取配置的麻烦。

另一种注入配置的方式是先通过一个简单的JavaBean持有所有的配置，例如，一个SmtpConfig：
```java
@Component
public class SmtpConfig {
    @Value("${smtp.host}")
    private String host;

    @Value("${smtp.port:25}")
    private int port;

    public String getHost() {
        return host;
    }

    public int getPort() {
        return port;
    }
}
```
然后，在需要读取的地方，使用#{smtpConfig.host}注入：
```java
@Component
public class MailService {
    @Value("#{smtpConfig.host}")
    private String smtpHost;

    @Value("#{smtpConfig.port}")
    private int smtpPort;
}
```
注意观察#{}这种注入语法，它和${key}不同的是，#{}表示从JavaBean读取属性。"#{smtpConfig.host}"的意思是，从名称为smtpConfig的Bean读取host属性，即调用getHost()方法。一个Class名为SmtpConfig的Bean，它在Spring容器中的默认名称就是smtpConfig，除非用@Qualifier指定了名称。

使用一个独立的JavaBean持有所有属性，然后在其他Bean中以#{bean.property}注入的好处是，多个Bean都可以引用同一个Bean的某个属性。例如，如果SmtpConfig决定从数据库中读取相关配置项，那么MailService注入的@Value("#{smtpConfig.host}")仍然可以不修改正常运行。

### 使用条件装配
开发应用程序时，我们会使用开发环境，例如，使用内存数据库以便快速启动。而运行在生产环境时，我们会使用生产环境，例如，使用MySQL数据库。如果应用程序可以根据自身的环境做一些适配，无疑会更加灵活。

Spring为应用程序准备了Profile这一概念，用来表示不同的环境。例如，我们分别定义开发、测试和生产这3个环境：

- native
- test
- production

创建某个Bean时，Spring容器可以根据注解@Profile来决定是否创建。例如，以下配置：
```java
@Configuration
@ComponentScan
public class AppConfig {
    @Bean
    @Profile("!test")
    ZoneId createZoneId() {
        return ZoneId.systemDefault();
    }

    @Bean
    @Profile("test")
    ZoneId createZoneIdForTest() {
        return ZoneId.of("America/New_York");
    }
}
```
如果当前的Profile设置为test，则Spring容器会调用createZoneIdForTest()创建ZoneId，否则，调用createZoneId()创建ZoneId。注意到@Profile("!test")表示非test环境。

在运行程序时，加上JVM参数-Dspring.profiles.active=test就可以指定以test环境启动。

实际上，Spring允许指定多个Profile，例如：-Dspring.profiles.active=test,master可以表示test环境，并使用master分支代码。

要满足多个Profile条件，可以这样写：
```java
@Bean
@Profile({ "test", "master" }) // 同时满足test和master
ZoneId createZoneId() {
    ...
}
```

#### 使用Conditional
除了根据@Profile条件来决定是否创建某个Bean外，Spring还可以根据@Conditional决定是否创建某个Bean。

例如，我们对SmtpMailService添加如下注解：
```java
@Component
@Conditional(OnSmtpEnvCondition.class)
public class SmtpMailService implements MailService {
    ...
}
```
它的意思是，如果满足OnSmtpEnvCondition的条件，才会创建SmtpMailService这个Bean。OnSmtpEnvCondition的条件是什么呢？我们看一下代码：
```java
public class OnSmtpEnvCondition implements Condition {
    public boolean matches(ConditionContext context, AnnotatedTypeMetadata metadata) {
        return "true".equalsIgnoreCase(System.getenv("smtp"));
    }
}
```
因此，OnSmtpEnvCondition的条件是存在环境变量smtp，值为true。这样，我们就可以通过环境变量来控制是否创建SmtpMailService。

Spring只提供了@Conditional注解，具体判断逻辑还需要我们自己实现。Spring Boot提供了更多使用起来更简单的条件注解，例如，如果配置文件中存在app.smtp=true，则创建MailService：
```java
@Component
@ConditionalOnProperty(name="app.smtp", havingValue="true")
public class MailService {
    ...
}
```
如果当前classpath中存在类javax.mail.Transport，则创建MailService：
```java
@Component
@ConditionalOnClass(name = "javax.mail.Transport")
public class MailService {
    ...
}
```
后续我们会介绍Spring Boot的条件装配。我们以文件存储为例，假设我们需要保存用户上传的头像，并返回存储路径，在本地开发运行时，我们总是存储到文件：
```java
@Component
@ConditionalOnProperty(name = "app.storage", havingValue = "file", matchIfMissing = true)
public class FileUploader implements Uploader {
    ...
}
```
在生产环境运行时，我们会把文件存储到类似AWS S3上：
```java
@Component
@ConditionalOnProperty(name = "app.storage", havingValue = "s3")
public class S3Uploader implements Uploader {
    ...
}
```
其他需要存储的服务则注入Uploader：
```java
@Component
public class UserImageService {
    @Autowired
    Uploader uploader;
}
```
当应用程序检测到配置文件存在app.storage=s3时，自动使用S3Uploader，如果存在配置app.storage=file，或者配置app.storage不存在，则使用FileUploader。

可见，使用条件注解，能更灵活地装配Bean。


## 使用AOP
AOP是Aspect Oriented Programming，即面向切面编程。那什么是AOP？我们先回顾一下OOP：Object Oriented Programming，OOP作为面向对象编程的模式，获得了巨大的成功，OOP的主要功能是数据封装、继承和多态。

而AOP是一种新的编程方式，它和OOP不同，OOP把系统看作多个对象的交互，AOP把系统分解为不同的关注点，或者称之为切面（Aspect）。

要理解AOP的概念，我们先用OOP举例，比如一个业务组件BookService，它有几个业务方法：

- createBook：添加新的Book；
- updateBook：修改Book；
- deleteBook：删除Book。

对每个业务方法，例如，createBook()，除了业务逻辑，还需要安全检查、日志记录和事务处理，它的代码像这样：
```java
public class BookService {
    public void createBook(Book book) {
        securityCheck();
        Transaction tx = startTransaction();
        try {
            // 核心业务逻辑
            tx.commit();
        } catch (RuntimeException e) {
            tx.rollback();
            throw e;
        }
        log("created book: " + book);
    }
}
```
继续编写updateBook()，代码如下：
```java
public class BookService {
    public void updateBook(Book book) {
        securityCheck();
        Transaction tx = startTransaction();
        try {
            // 核心业务逻辑
            tx.commit();
        } catch (RuntimeException e) {
            tx.rollback();
            throw e;
        }
        log("updated book: " + book);
    }
}
```
对于安全检查、日志、事务等代码，它们会重复出现在每个业务方法中。使用OOP，我们很难将这些四处分散的代码模块化。

考察业务模型可以发现，BookService关心的是自身的核心逻辑，但整个系统还要求关注安全检查、日志、事务等功能，这些功能实际上“横跨”多个业务方法，为了实现这些功能，不得不在每个业务方法上重复编写代码。

一种可行的方式是使用Proxy模式，将某个功能，例如，权限检查，放入Proxy中：
```java
public class SecurityCheckBookService implements BookService {
    private final BookService target;

    public SecurityCheckBookService(BookService target) {
        this.target = target;
    }

    public void createBook(Book book) {
        securityCheck();
        target.createBook(book);
    }

    public void updateBook(Book book) {
        securityCheck();
        target.updateBook(book);
    }

    public void deleteBook(Book book) {
        securityCheck();
        target.deleteBook(book);
    }

    private void securityCheck() {
        ...
    }
}
```
这种方式的缺点是比较麻烦，必须先抽取接口，然后，针对每个方法实现Proxy。

另一种方法是，既然SecurityCheckBookService的代码都是标准的Proxy样板代码，不如把权限检查视作一种切面（Aspect），把日志、事务也视为切面，然后，以某种自动化的方式，把切面织入到核心逻辑中，实现Proxy模式。

如果我们以AOP的视角来编写上述业务，可以依次实现：

- 核心逻辑，即BookService；
- 切面逻辑，即：
- 权限检查的Aspect；
- 日志的Aspect；
- 事务的Aspect。

然后，以某种方式，让框架来把上述3个Aspect以Proxy的方式“织入”到BookService中，这样一来，就不必编写复杂而冗长的Proxy模式。

#### AOP原理
如何把切面织入到核心逻辑中？这正是AOP需要解决的问题。换句话说，如果客户端获得了BookService的引用，当调用bookService.createBook()时，如何对调用方法进行拦截，并在拦截前后进行安全检查、日志、事务等处理，就相当于完成了所有业务功能。

在Java平台上，对于AOP的织入，有3种方式：

1. 编译期：在编译时，由编译器把切面调用编译进字节码，这种方式需要定义新的关键字并扩展编译器，AspectJ就扩展了Java编译器，使用关键字aspect来实现织入；
2. 类加载器：在目标类被装载到JVM时，通过一个特殊的类加载器，对目标类的字节码重新“增强”；
3. 运行期：目标对象和切面都是普通Java类，通过JVM的动态代理功能或者第三方库实现运行期动态织入。

最简单的方式是第三种，Spring的AOP实现就是基于JVM的动态代理。由于JVM的动态代理要求必须实现接口，如果一个普通类没有业务接口，就需要通过CGLIB或者Javassist这些第三方库实现。

AOP技术看上去比较神秘，但实际上，它本质就是一个动态代理，让我们把一些常用功能如权限检查、日志、事务等，从每个业务方法中剥离出来。

需要特别指出的是，AOP对于解决特定问题，例如事务管理非常有用，这是因为分散在各处的事务代码几乎是完全相同的，并且它们需要的参数（JDBC的Connection）也是固定的。另一些特定问题，如日志，就不那么容易实现，因为日志虽然简单，但打印日志的时候，经常需要捕获局部变量，如果使用AOP实现日志，我们只能输出固定格式的日志，因此，使用AOP时，必须适合特定的场景。

### 装配AOP
在AOP编程中，我们经常会遇到下面的概念：

- Aspect：切面，即一个横跨多个核心逻辑的功能，或者称之为系统关注点；
- Joinpoint：连接点，即定义在应用程序流程的何处插入切面的执行；
- Pointcut：切入点，即一组连接点的集合；
- Advice：增强，指特定连接点上执行的动作；
- Introduction：引介，指为一个已有的Java对象动态地增加新的接口；
- Weaving：织入，指将切面整合到程序的执行流程中；
- Interceptor：拦截器，是一种实现增强的方式；
- Target Object：目标对象，即真正执行业务的核心逻辑对象；
- AOP Proxy：AOP代理，是客户端持有的增强后的对象引用。

看完上述术语，是不是感觉对AOP有了进一步的困惑？其实，我们不用关心AOP创造的“术语”，只需要理解AOP本质上只是一种代理模式的实现方式，在Spring的容器中实现AOP特别方便。

我们以UserService和MailService为例，这两个属于核心业务逻辑，现在，我们准备给UserService的每个业务方法执行前添加日志，给MailService的每个业务方法执行前后添加日志，在Spring中，需要以下步骤：

首先，我们通过Maven引入Spring对AOP的支持：
```xml
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-aspects</artifactId>
    <version>${spring.version}</version>
</dependency>
```
上述依赖会自动引入AspectJ，使用AspectJ实现AOP比较方便，因为它的定义比较简单。

然后，我们定义一个LoggingAspect：
```java
@Aspect
@Component
public class LoggingAspect {
    // 在执行UserService的每个方法前执行:
    @Before("execution(public * com.itranswarp.learnjava.service.UserService.*(..))")
    public void doAccessCheck() {
        System.err.println("[Before] do access check...");
    }

    // 在执行MailService的每个方法前后执行:
    @Around("execution(public * com.itranswarp.learnjava.service.MailService.*(..))")
    public Object doLogging(ProceedingJoinPoint pjp) throws Throwable {
        System.err.println("[Around] start " + pjp.getSignature());
        Object retVal = pjp.proceed();
        System.err.println("[Around] done " + pjp.getSignature());
        return retVal;
    }
}
```
观察doAccessCheck()方法，我们定义了一个@Before注解，后面的字符串是告诉AspectJ应该在何处执行该方法，这里写的意思是：执行UserService的每个public方法前执行doAccessCheck()代码。

再观察doLogging()方法，我们定义了一个@Around注解，它和@Before不同，@Around可以决定是否执行目标方法，因此，我们在doLogging()内部先打印日志，再调用方法，最后打印日志后返回结果。

在LoggingAspect类的声明处，除了用@Component表示它本身也是一个Bean外，我们再加上@Aspect注解，表示它的@Before标注的方法需要注入到UserService的每个public方法执行前，@Around标注的方法需要注入到MailService的每个public方法执行前后。

紧接着，我们需要给@Configuration类加上一个@EnableAspectJAutoProxy注解：
```java
@Configuration
@ComponentScan
@EnableAspectJAutoProxy
public class AppConfig {
    ...
}
```
Spring的IoC容器看到这个注解，就会自动查找带有@Aspect的Bean，然后根据每个方法的@Before、@Around等注解把AOP注入到特定的Bean中。执行代码，我们可以看到以下输出：
```
[Before] do access check...
[Around] start void com.itranswarp.learnjava.service.MailService.sendRegistrationMail(User)
Welcome, test!
[Around] done void com.itranswarp.learnjava.service.MailService.sendRegistrationMail(User)
[Before] do access check...
[Around] start void com.itranswarp.learnjava.service.MailService.sendLoginMail(User)
Hi, Bob! You are logged in at 2020-02-14T23:13:52.167996+08:00[Asia/Shanghai]
[Around] done void com.itranswarp.learnjava.service.MailService.sendLoginMail(User)
```
这说明执行业务逻辑前后，确实执行了我们定义的Aspect（即LoggingAspect的方法）。

有些童鞋会问，LoggingAspect定义的方法，是如何注入到其他Bean的呢？

其实AOP的原理非常简单。我们以LoggingAspect.doAccessCheck()为例，要把它注入到UserService的每个public方法中，最简单的方法是编写一个子类，并持有原始实例的引用：
```java
public UserServiceAopProxy extends UserService {
    private UserService target;
    private LoggingAspect aspect;

    public UserServiceAopProxy(UserService target, LoggingAspect aspect) {
        this.target = target;
        this.aspect = aspect;
    }

    public User login(String email, String password) {
        // 先执行Aspect的代码:
        aspect.doAccessCheck();
        // 再执行UserService的逻辑:
        return target.login(email, password);
    }

    public User register(String email, String password, String name) {
        aspect.doAccessCheck();
        return target.register(email, password, name);
    }

    ...
}
```
这些都是Spring容器启动时为我们自动创建的注入了Aspect的子类，它取代了原始的UserService（原始的UserService实例作为内部变量隐藏在UserServiceAopProxy中）。如果我们打印从Spring容器获取的UserService实例类型，它类似`UserService$$EnhancerBySpringCGLIB$$1f44e01c`，实际上是Spring使用CGLIB动态创建的子类，但对于调用方来说，感觉不到任何区别。

Spring对接口类型使用JDK动态代理，对普通类使用CGLIB创建子类。如果一个Bean的class是final，Spring将无法为其创建子类。
可见，虽然Spring容器内部实现AOP的逻辑比较复杂（需要使用AspectJ解析注解，并通过CGLIB实现代理类），但我们使用AOP非常简单，一共需要三步：

- 定义执行方法，并在方法上通过AspectJ的注解告诉Spring应该在何处调用此方法；
- 标记@Component和@Aspect；
- 在@Configuration类上标注@EnableAspectJAutoProxy。

Spring也提供其他方法来装配AOP，但都没有使用AspectJ注解的方式来得简洁明了，所以我们不再作介绍。

#### 拦截器类型
顾名思义，拦截器有以下类型：

- @Before：这种拦截器先执行拦截代码，再执行目标代码。如果拦截器抛异常，那么目标代码就不执行了；
- @After：这种拦截器先执行目标代码，再执行拦截器代码。无论目标代码是否抛异常，拦截器代码都会执行；
- @AfterReturning：和@After不同的是，只有当目标代码正常返回时，才执行拦截器代码；
- @AfterThrowing：和@After不同的是，只有当目标代码抛出了异常时，才执行拦截器代码；
- @Around：能完全控制目标代码是否执行，并可以在执行前后、抛异常后执行任意拦截代码，可以说是包含了上面所有功能。

### 使用注解装配AOP
上一节我们讲解了使用AspectJ的注解，并配合一个复杂的execution(* xxx.Xyz.*(..))语法来定义应该如何装配AOP。

在实际项目中，这种写法其实很少使用。假设你写了一个SecurityAspect：
```java
@Aspect
@Component
public class SecurityAspect {
    @Before("execution(public * com.itranswarp.learnjava.service.*.*(..))")
    public void check() {
        if (SecurityContext.getCurrentUser() == null) {
            throw new RuntimeException("check failed");
        }
    }
}
```
基本能实现无差别全覆盖，即某个包下面的所有Bean的所有方法都会被这个check()方法拦截。

还有的童鞋喜欢用方法名前缀进行拦截：
```java
@Around("execution(public * update*(..))")
public Object doLogging(ProceedingJoinPoint pjp) throws Throwable {
    // 对update开头的方法切换数据源:
    String old = setCurrentDataSource("master");
    Object retVal = pjp.proceed();
    restoreCurrentDataSource(old);
    return retVal;
}
```
这种非精准打击误伤面更大，因为从方法前缀区分是否是数据库操作是非常不可取的。

我们在使用AOP时，要注意到虽然Spring容器可以把指定的方法通过AOP规则装配到指定的Bean的指定方法前后，但是，如果自动装配时，因为不恰当的范围，容易导致意想不到的结果，即很多不需要AOP代理的Bean也被自动代理了，并且，后续新增的Bean，如果不清楚现有的AOP装配规则，容易被强迫装配。

使用AOP时，被装配的Bean最好自己能清清楚楚地知道自己被安排了。例如，Spring提供的@Transactional就是一个非常好的例子。如果我们自己写的Bean希望在一个数据库事务中被调用，就标注上@Transactional：
```java
@Component
public class UserService {
    // 有事务:
    @Transactional
    public User createUser(String name) {
        ...
    }

    // 无事务:
    public boolean isValidName(String name) {
        ...
    }

    // 有事务:
    @Transactional
    public void updateUser(User user) {
        ...
    }
}
```
或者直接在class级别注解，表示“所有public方法都被安排了”：
```java
@Component
@Transactional
public class UserService {
    ...
}
```
通过@Transactional，某个方法是否启用了事务就一清二楚了。因此，装配AOP的时候，使用注解是最好的方式。

我们以一个实际例子演示如何使用注解实现AOP装配。为了监控应用程序的性能，我们定义一个性能监控的注解：
```java
@Target(METHOD)
@Retention(RUNTIME)
public @interface MetricTime {
    String value();
}
```
在需要被监控的关键方法上标注该注解：
```java
@Component
public class UserService {
    // 监控register()方法性能:
    @MetricTime("register")
    public User register(String email, String password, String name) {
        ...
    }
    ...
}
```
然后，我们定义MetricAspect：
```java
@Aspect
@Component
public class MetricAspect {
    @Around("@annotation(metricTime)")
    public Object metric(ProceedingJoinPoint joinPoint, MetricTime metricTime) throws Throwable {
        String name = metricTime.value();
        long start = System.currentTimeMillis();
        try {
            return joinPoint.proceed();
        } finally {
            long t = System.currentTimeMillis() - start;
            // 写入日志或发送至JMX:
            System.err.println("[Metrics] " + name + ": " + t + "ms");
        }
    }
}
```
注意metric()方法标注了@Around("@annotation(metricTime)")，它的意思是，符合条件的目标方法是带有@MetricTime注解的方法，因为metric()方法参数类型是MetricTime（注意参数名是metricTime不是MetricTime），我们通过它获取性能监控的名称。

有了@MetricTime注解，再配合MetricAspect，任何Bean，只要方法标注了@MetricTime注解，就可以自动实现性能监控。运行代码，输出结果如下：
```
Welcome, Bob!
[Metrics] register: 16ms
```

### AOP避坑指南
无论是使用AspectJ语法，还是配合Annotation，使用AOP，实际上就是让Spring自动为我们创建一个Proxy，使得调用方能无感知地调用指定方法，但运行期却动态“织入”了其他逻辑，因此，AOP本质上就是一个代理模式。

因为Spring使用了CGLIB来实现运行期动态创建Proxy，如果我们没能深入理解其运行原理和实现机制，就极有可能遇到各种诡异的问题。

我们来看一个实际的例子。假设我们定义了一个UserService的Bean：
```java
@Component
public class UserService {
    // 成员变量:
    public final ZoneId zoneId = ZoneId.systemDefault();

    // 构造方法:
    public UserService() {
        System.out.println("UserService(): init...");
        System.out.println("UserService(): zoneId = " + this.zoneId);
    }

    // public方法:
    public ZoneId getZoneId() {
        return zoneId;
    }

    // public final方法:
    public final ZoneId getFinalZoneId() {
        return zoneId;
    }
}
```
再写个MailService，并注入UserService：
```java
@Component
public class MailService {
    @Autowired
    UserService userService;

    public String sendMail() {
        ZoneId zoneId = userService.zoneId;
        String dt = ZonedDateTime.now(zoneId).toString();
        return "Hello, it is " + dt;
    }
}
```
最后用main()方法测试一下：
```java
@Configuration
@ComponentScan
public class AppConfig {
    public static void main(String[] args) {
        ApplicationContext context = new AnnotationConfigApplicationContext(AppConfig.class);
        MailService mailService = context.getBean(MailService.class);
        System.out.println(mailService.sendMail());
    }
}
```
查看输出，一切正常：
```
UserService(): init...
UserService(): zoneId = Asia/Shanghai
Hello, it is 2020-04-12T10:23:22.917721+08:00[Asia/Shanghai]
```
下一步，我们给UserService加上AOP支持，就添加一个最简单的LoggingAspect：
```java
@Aspect
@Component
public class LoggingAspect {
    @Before("execution(public * com..*.UserService.*(..))")
    public void doAccessCheck() {
        System.err.println("[Before] do access check...");
    }
}
```
别忘了在AppConfig上加上@EnableAspectJAutoProxy。再次运行，不出意外的话，会得到一个NullPointerException：
```
Exception in thread "main" java.lang.NullPointerException: zone
    at java.base/java.util.Objects.requireNonNull(Objects.java:246)
    at java.base/java.time.Clock.system(Clock.java:203)
    at java.base/java.time.ZonedDateTime.now(ZonedDateTime.java:216)
    at com.itranswarp.learnjava.service.MailService.sendMail(MailService.java:19)
    at com.itranswarp.learnjava.AppConfig.main(AppConfig.java:21)
```
仔细跟踪代码，会发现null值出现在MailService.sendMail()内部的这一行代码：
```java
@Component
public class MailService {
    @Autowired
    UserService userService;

    public String sendMail() {
        ZoneId zoneId = userService.zoneId;
        System.out.println(zoneId); // null
        ...
    }
}
```
我们还故意在UserService中特意用final修饰了一下成员变量：
```java
@Component
public class UserService {
    public final ZoneId zoneId = ZoneId.systemDefault();
    ...
}
```
用final标注的成员变量为null？为什么加了AOP就报NPE，去了AOP就一切正常？final字段不执行，难道JVM有问题？为了解答这个诡异的问题，我们需要深入理解Spring使用CGLIB生成Proxy的原理：

第一步，正常创建一个UserService的原始实例，这是通过反射调用构造方法实现的，它的行为和我们预期的完全一致；

第二步，通过CGLIB创建一个UserService的子类，并引用了原始实例和LoggingAspect：
```java
public UserService$$EnhancerBySpringCGLIB extends UserService {
    UserService target;
    LoggingAspect aspect;

    public UserService$$EnhancerBySpringCGLIB() {
    }

    public ZoneId getZoneId() {
        aspect.doAccessCheck();
        return target.getZoneId();
    }
}
```

如果我们观察Spring创建的AOP代理，它的类名总是类似UserService$$EnhancerBySpringCGLIB$$1c76af9d（你没看错，Java的类名实际上允许$字符）。为了让调用方获得UserService的引用，它必须继承自UserService。然后，该代理类会覆写所有public和protected方法，并在内部将调用委托给原始的UserService实例。

这里出现了两个UserService实例：

一个是我们代码中定义的原始实例，它的成员变量已经按照我们预期的方式被初始化完成：`UserService original = new UserService();`

第二个UserService实例实际上类型是`UserService$$EnhancerBySpringCGLIB`，它引用了原始的UserService实例：
```java
UserService$$EnhancerBySpringCGLIB proxy = new UserService$$EnhancerBySpringCGLIB();
proxy.target = original;
proxy.aspect = ...
```
注意到这种情况仅出现在启用了AOP的情况，此刻，从ApplicationContext中获取的UserService实例是proxy，注入到MailService中的UserService实例也是proxy。

那么最终的问题来了：proxy实例的成员变量，也就是从UserService继承的zoneId，它的值是null。

原因在于，UserService成员变量的初始化：
```java
public class UserService {
    public final ZoneId zoneId = ZoneId.systemDefault();
    ...
}
```
在`UserService$$EnhancerBySpringCGLIB`中，并未执行。原因是，没必要初始化proxy的成员变量，因为proxy的目的是代理方法。

实际上，成员变量的初始化是在构造方法中完成的。这是我们看到的代码：
```java
public class UserService {
    public final ZoneId zoneId = ZoneId.systemDefault();
    public UserService() {
    }
}
```
这是编译器实际编译的代码：
```java
public class UserService {
    public final ZoneId zoneId;
    public UserService() {
        super(); // 构造方法的第一行代码总是调用super()
        zoneId = ZoneId.systemDefault(); // 继续初始化成员变量
    }
}
```
然而，对于Spring通过CGLIB动态创建的`UserService$$EnhancerBySpringCGLIB`代理类，它的构造方法中，并未调用super()，因此，从父类继承的成员变量，包括final类型的成员变量，统统都没有初始化。

有的童鞋会问：Java语言规定，任何类的构造方法，第一行必须调用super()，如果没有，编译器会自动加上，怎么Spring的CGLIB就可以搞特殊？

这是因为自动加super()的功能是Java编译器实现的，它发现你没加，就自动给加上，发现你加错了，就报编译错误。但实际上，如果直接构造字节码，一个类的构造方法中，不一定非要调用super()。Spring使用CGLIB构造的Proxy类，是直接生成字节码，并没有源码-编译-字节码这个步骤，因此：

Spring通过CGLIB创建的代理类，不会初始化代理类自身继承的任何成员变量，包括final类型的成员变量！
再考察MailService的代码：
```java
@Component
public class MailService {
    @Autowired
    UserService userService;

    public String sendMail() {
        ZoneId zoneId = userService.zoneId;
        System.out.println(zoneId); // null
        ...
    }
}
```
如果没有启用AOP，注入的是原始的UserService实例，那么一切正常，因为UserService实例的zoneId字段已经被正确初始化了。

如果启动了AOP，注入的是代理后的UserService$$EnhancerBySpringCGLIB实例，那么问题大了：获取的UserService$$EnhancerBySpringCGLIB实例的zoneId字段，永远为null。

那么问题来了：启用了AOP，如何修复？

修复很简单，只需要把直接访问字段的代码，改为通过方法访问：
```java
@Component
public class MailService {
    @Autowired
    UserService userService;

    public String sendMail() {
        // 不要直接访问UserService的字段:
        ZoneId zoneId = userService.getZoneId();
        ...
    }
}
```
无论注入的UserService是原始实例还是代理实例，getZoneId()都能正常工作，因为代理类会覆写getZoneId()方法，并将其委托给原始实例：
```java
public UserService$$EnhancerBySpringCGLIB extends UserService {
    UserService target = ...
    ...

    public ZoneId getZoneId() {
        return target.getZoneId();
    }
}
```
注意到我们还给UserService添加了一个public+final的方法：
```java
@Component
public class UserService {
    ...
    public final ZoneId getFinalZoneId() {
        return zoneId;
    }
}
```
如果在MailService中，调用的不是getZoneId()，而是getFinalZoneId()，又会出现NullPointerException，这是因为，代理类无法覆写final方法（这一点绕不过JVM的ClassLoader检查），该方法返回的是代理类的zoneId字段，即null。

实际上，如果我们加上日志，Spring在启动时会打印一个警告：
```
10:43:09.929 [main] DEBUG org.springframework.aop.framework.CglibAopProxy - Final method [public final java.time.ZoneId xxx.UserService.getFinalZoneId()] cannot get proxied via CGLIB: Calls to this method will NOT be routed to the target instance and might lead to NPEs against uninitialized fields in the proxy instance.
```
上面的日志大意就是，因为被代理的UserService有一个final方法getFinalZoneId()，这会导致其他Bean如果调用此方法，无法将其代理到真正的原始实例，从而可能发生NPE异常。

因此，正确使用AOP，我们需要一个避坑指南：

- 访问被注入的Bean时，总是调用方法而非直接访问字段；
- 编写Bean时，如果可能会被代理，就不要编写public final方法。

这样才能保证有没有AOP，代码都能正常工作。


## 访问数据库
数据库基本上是现代应用程序的标准存储，绝大多数程序都把自己的业务数据存储在关系数据库中，可见，访问数据库几乎是所有应用程序必备能力。

我们在前面已经介绍了Java程序访问数据库的标准接口JDBC，它的实现方式非常简洁，即：Java标准库定义接口，各数据库厂商以“驱动”的形式实现接口。应用程序要使用哪个数据库，就把该数据库厂商的驱动以jar包形式引入进来，同时自身仅使用JDBC接口，编译期并不需要特定厂商的驱动。

使用JDBC虽然简单，但代码比较繁琐。Spring为了简化数据库访问，主要做了以下几点工作：

- 提供了简化的访问JDBC的模板类，不必手动释放资源；
- 提供了一个统一的DAO类以实现Data Access Object模式；
- 把SQLException封装为DataAccessException，这个异常是一个RuntimeException，并且让我们能区分SQL异常的原因，例如，DuplicateKeyException表示违反了一个唯一约束；
- 能方便地集成Hibernate、JPA和MyBatis这些数据库访问框架。

### 使用JDBC
我们在前面介绍JDBC编程时已经讲过，Java程序使用JDBC接口访问关系数据库的时候，需要以下几步：

- 创建全局DataSource实例，表示数据库连接池；
- 在需要读写数据库的方法内部，按如下步骤访问数据库：
- 从全局DataSource实例获取Connection实例；
- 通过Connection实例创建PreparedStatement实例；
- 执行SQL语句，如果是查询，则通过ResultSet读取结果集，如果是修改，则获得int结果。
- 正确编写JDBC代码的关键是使用try ... finally释放资源，涉及到事务的代码需要正确提交或回滚事务。

在Spring使用JDBC，首先我们通过IoC容器创建并管理一个DataSource实例，然后，Spring提供了一个JdbcTemplate，可以方便地让我们操作JDBC，因此，通常情况下，我们会实例化一个JdbcTemplate。顾名思义，这个类主要使用了Template模式。

编写示例代码或者测试代码时，我们强烈推荐使用HSQLDB这个数据库，它是一个用Java编写的关系数据库，可以以内存模式或者文件模式运行，本身只有一个jar包，非常适合演示代码或者测试代码。

我们以实际工程为例，先创建Maven工程spring-data-jdbc，然后引入以下依赖：
```xml
<dependencies>
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-context</artifactId>
        <version>5.2.0.RELEASE</version>
    </dependency>
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-jdbc</artifactId>
        <version>5.2.0.RELEASE</version>
    </dependency>
    <dependency>
        <groupId>javax.annotation</groupId>
        <artifactId>javax.annotation-api</artifactId>
        <version>1.3.2</version>
    </dependency>
    <dependency>
        <groupId>com.zaxxer</groupId>
        <artifactId>HikariCP</artifactId>
        <version>3.4.2</version>
    </dependency>
    <dependency>
        <groupId>org.hsqldb</groupId>
        <artifactId>hsqldb</artifactId>
        <version>2.5.0</version>
    </dependency>
</dependencies>
```
在AppConfig中，我们需要创建以下几个必须的Bean：
```java
@Configuration
@ComponentScan
@PropertySource("jdbc.properties")
public class AppConfig {

    @Value("${jdbc.url}")
    String jdbcUrl;

    @Value("${jdbc.username}")
    String jdbcUsername;

    @Value("${jdbc.password}")
    String jdbcPassword;

    @Bean
    DataSource createDataSource() {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl(jdbcUrl);
        config.setUsername(jdbcUsername);
        config.setPassword(jdbcPassword);
        config.addDataSourceProperty("autoCommit", "true");
        config.addDataSourceProperty("connectionTimeout", "5");
        config.addDataSourceProperty("idleTimeout", "60");
        return new HikariDataSource(config);
    }

    @Bean
    JdbcTemplate createJdbcTemplate(@Autowired DataSource dataSource) {
        return new JdbcTemplate(dataSource);
    }
}
```
在上述配置中：

- 通过@PropertySource("jdbc.properties")读取数据库配置文件；
- 通过@Value("${jdbc.url}")注入配置文件的相关配置；
- 创建一个DataSource实例，它的实际类型是HikariDataSource，创建时需要用到注入的配置；
- 创建一个JdbcTemplate实例，它需要注入DataSource，这是通过方法参数完成注入的。

最后，针对HSQLDB写一个配置文件jdbc.properties：
```
# 数据库文件名为testdb:
jdbc.url=jdbc:hsqldb:file:testdb

# Hsqldb默认的用户名是sa，口令是空字符串:
jdbc.username=sa
jdbc.password=
```
可以通过HSQLDB自带的工具来初始化数据库表，这里我们写一个Bean，在Spring容器启动时自动创建一个users表：
```java
@Component
public class DatabaseInitializer {
    @Autowired
    JdbcTemplate jdbcTemplate;

    @PostConstruct
    public void init() {
        jdbcTemplate.update("CREATE TABLE IF NOT EXISTS users (" //
                + "id BIGINT IDENTITY NOT NULL PRIMARY KEY, " //
                + "email VARCHAR(100) NOT NULL, " //
                + "password VARCHAR(100) NOT NULL, " //
                + "name VARCHAR(100) NOT NULL, " //
                + "UNIQUE (email))");
    }
}
```
现在，所有准备工作都已完毕。我们只需要在需要访问数据库的Bean中，注入JdbcTemplate即可：
```java
@Component
public class UserService {
    @Autowired
    JdbcTemplate jdbcTemplate;
    ...
}
```

#### JdbcTemplate用法
Spring提供的JdbcTemplate采用Template模式，提供了一系列以回调为特点的工具方法，目的是避免繁琐的try...catch语句。

我们以具体的示例来说明JdbcTemplate的用法。

首先我们看T execute(ConnectionCallback<T> action)方法，它提供了Jdbc的Connection供我们使用：
```java
public User getUserById(long id) {
    // 注意传入的是ConnectionCallback:
    return jdbcTemplate.execute((Connection conn) -> {
        // 可以直接使用conn实例，不要释放它，回调结束后JdbcTemplate自动释放:
        // 在内部手动创建的PreparedStatement、ResultSet必须用try(...)释放:
        try (var ps = conn.prepareStatement("SELECT * FROM users WHERE id = ?")) {
            ps.setObject(1, id);
            try (var rs = ps.executeQuery()) {
                if (rs.next()) {
                    return new User( // new User object:
                            rs.getLong("id"), // id
                            rs.getString("email"), // email
                            rs.getString("password"), // password
                            rs.getString("name")); // name
                }
                throw new RuntimeException("user not found by id.");
            }
        }
    });
}
```
也就是说，上述回调方法允许获取Connection，然后做任何基于Connection的操作。

我们再看T execute(String sql, PreparedStatementCallback<T> action)的用法：
```java
public User getUserByName(String name) {
    // 需要传入SQL语句，以及PreparedStatementCallback:
    return jdbcTemplate.execute("SELECT * FROM users WHERE name = ?", (PreparedStatement ps) -> {
        // PreparedStatement实例已经由JdbcTemplate创建，并在回调后自动释放:
        ps.setObject(1, name);
        try (var rs = ps.executeQuery()) {
            if (rs.next()) {
                return new User( // new User object:
                        rs.getLong("id"), // id
                        rs.getString("email"), // email
                        rs.getString("password"), // password
                        rs.getString("name")); // name
            }
            throw new RuntimeException("user not found by id.");
        }
    });
}
```
最后，我们看T queryForObject(String sql, Object[] args, RowMapper<T> rowMapper)方法：
```java
public User getUserByEmail(String email) {
    // 传入SQL，参数和RowMapper实例:
    return jdbcTemplate.queryForObject("SELECT * FROM users WHERE email = ?", new Object[] { email },
            (ResultSet rs, int rowNum) -> {
                // 将ResultSet的当前行映射为一个JavaBean:
                return new User( // new User object:
                        rs.getLong("id"), // id
                        rs.getString("email"), // email
                        rs.getString("password"), // password
                        rs.getString("name")); // name
            });
}
```
在queryForObject()方法中，传入SQL以及SQL参数后，JdbcTemplate会自动创建PreparedStatement，自动执行查询并返回ResultSet，我们提供的RowMapper需要做的事情就是把ResultSet的当前行映射成一个JavaBean并返回。整个过程中，使用Connection、PreparedStatement和ResultSet都不需要我们手动管理。

RowMapper不一定返回JavaBean，实际上它可以返回任何Java对象。例如，使用SELECT COUNT(*)查询时，可以返回Long：
```java
public long getUsers() {
    return jdbcTemplate.queryForObject("SELECT COUNT(*) FROM users", null, (ResultSet rs, int rowNum) -> {
        // SELECT COUNT(*)查询只有一列，取第一列数据:
        return rs.getLong(1);
    });
}
```
如果我们期望返回多行记录，而不是一行，可以用query()方法：
```java
public List<User> getUsers(int pageIndex) {
    int limit = 100;
    int offset = limit * (pageIndex - 1);
    return jdbcTemplate.query("SELECT * FROM users LIMIT ? OFFSET ?", new Object[] { limit, offset },
            new BeanPropertyRowMapper<>(User.class));
}
```
上述query()方法传入的参数仍然是SQL、SQL参数以及RowMapper实例。这里我们直接使用Spring提供的BeanPropertyRowMapper。如果数据库表的结构恰好和JavaBean的属性名称一致，那么BeanPropertyRowMapper就可以直接把一行记录按列名转换为JavaBean。

如果我们执行的不是查询，而是插入、更新和删除操作，那么需要使用update()方法：
```java
public void updateUser(User user) {
    // 传入SQL，SQL参数，返回更新的行数:
    if (1 != jdbcTemplate.update("UPDATE user SET name = ? WHERE id=?", user.getName(), user.getId())) {
        throw new RuntimeException("User not found by id");
    }
}
```
只有一种INSERT操作比较特殊，那就是如果某一列是自增列（例如自增主键），通常，我们需要获取插入后的自增值。JdbcTemplate提供了一个KeyHolder来简化这一操作：
```java
public User register(String email, String password, String name) {
    // 创建一个KeyHolder:
    KeyHolder holder = new GeneratedKeyHolder();
    if (1 != jdbcTemplate.update(
        // 参数1:PreparedStatementCreator
        (conn) -> {
            // 创建PreparedStatement时，必须指定RETURN_GENERATED_KEYS:
            var ps = conn.prepareStatement("INSERT INTO users(email,password,name) VALUES(?,?,?)",
                    Statement.RETURN_GENERATED_KEYS);
            ps.setObject(1, email);
            ps.setObject(2, password);
            ps.setObject(3, name);
            return ps;
        },
        // 参数2:KeyHolder
        holder)
    ) {
        throw new RuntimeException("Insert failed.");
    }
    // 从KeyHolder中获取返回的自增值:
    return new User(holder.getKey().longValue(), email, password, name);
}
```
JdbcTemplate还有许多重载方法，这里我们不一一介绍。需要强调的是，JdbcTemplate只是对JDBC操作的一个简单封装，它的目的是尽量减少手动编写try(resource) {...}的代码，对于查询，主要通过RowMapper实现了JDBC结果集到Java对象的转换。

我们总结一下JdbcTemplate的用法，那就是：

- 针对简单查询，优选query()和queryForObject()，因为只需提供SQL语句、参数和RowMapper；
- 针对更新操作，优选update()，因为只需提供SQL语句和参数；
- 任何复杂的操作，最终也可以通过execute(ConnectionCallback)实现，因为拿到Connection就可以做任何JDBC操作。

实际上我们使用最多的仍然是各种查询。如果在设计表结构的时候，能够和JavaBean的属性一一对应，那么直接使用BeanPropertyRowMapper就很方便。如果表结构和JavaBean不一致怎么办？那就需要稍微改写一下查询，使结果集的结构和JavaBean保持一致。

例如，表的列名是office_address，而JavaBean属性是workAddress，就需要指定别名，改写查询如下：
```sql
SELECT id, email, office_address AS workAddress, name FROM users WHERE email = ?
```

###  使用声明式事务
使用Spring操作JDBC虽然方便，但是我们在前面讨论JDBC的时候，讲到过JDBC事务，如果要在Spring中操作事务，没必要手写JDBC事务，可以使用Spring提供的高级接口来操作事务。

Spring提供了一个PlatformTransactionManager来表示事务管理器，所有的事务都由它负责管理。而事务由TransactionStatus表示。如果手写事务代码，使用try...catch如下：
```java
TransactionStatus tx = null;
try {
    // 开启事务:
    tx = txManager.getTransaction(new DefaultTransactionDefinition());
    // 相关JDBC操作:
    jdbcTemplate.update("...");
    jdbcTemplate.update("...");
    // 提交事务:
    txManager.commit(tx);
} catch (RuntimeException e) {
    // 回滚事务:
    txManager.rollback(tx);
    throw e;
}
```
Spring为啥要抽象出PlatformTransactionManager和TransactionStatus？原因是JavaEE除了提供JDBC事务外，它还支持分布式事务JTA（Java Transaction API）。分布式事务是指多个数据源（比如多个数据库，多个消息系统）要在分布式环境下实现事务的时候，应该怎么实现。分布式事务实现起来非常复杂，简单地说就是通过一个分布式事务管理器实现两阶段提交，但本身数据库事务就不快，基于数据库事务实现的分布式事务就慢得难以忍受，所以使用率不高。

Spring为了同时支持JDBC和JTA两种事务模型，就抽象出PlatformTransactionManager。因为我们的代码只需要JDBC事务，因此，在AppConfig中，需要再定义一个PlatformTransactionManager对应的Bean，它的实际类型是DataSourceTransactionManager：
```java
@Configuration
@ComponentScan
@PropertySource("jdbc.properties")
public class AppConfig {
    ...
    @Bean
    PlatformTransactionManager createTxManager(@Autowired DataSource dataSource) {
        return new DataSourceTransactionManager(dataSource);
    }
}
```
使用编程的方式使用Spring事务仍然比较繁琐，更好的方式是通过声明式事务来实现。使用声明式事务非常简单，除了在AppConfig中追加一个上述定义的PlatformTransactionManager外，再加一个@EnableTransactionManagement就可以启用声明式事务：
```java
@Configuration
@ComponentScan
@EnableTransactionManagement // 启用声明式
@PropertySource("jdbc.properties")
public class AppConfig {
    ...
}
```
然后，对需要事务支持的方法，加一个@Transactional注解：
```java
@Component
public class UserService {
    // 此public方法自动具有事务支持:
    @Transactional
    public User register(String email, String password, String name) {
       ...
    }
}
```
或者更简单一点，直接在Bean的class处加上，表示所有public方法都具有事务支持：
```java
@Component
@Transactional
public class UserService {
    ...
}
```
Spring对一个声明式事务的方法，如何开启事务支持？原理仍然是AOP代理，即通过自动创建Bean的Proxy实现：
```java
public class UserService$$EnhancerBySpringCGLIB extends UserService {
    UserService target = ...
    PlatformTransactionManager txManager = ...

    public User register(String email, String password, String name) {
        TransactionStatus tx = null;
        try {
            tx = txManager.getTransaction(new DefaultTransactionDefinition());
            target.register(email, password, name);
            txManager.commit(tx);
        } catch (RuntimeException e) {
            txManager.rollback(tx);
            throw e;
        }
    }
    ...
}
```
注意：声明了@EnableTransactionManagement后，不必额外添加@EnableAspectJAutoProxy。

#### 回滚事务
默认情况下，如果发生了RuntimeException，Spring的声明式事务将自动回滚。在一个事务方法中，如果程序判断需要回滚事务，只需抛出RuntimeException，例如：
```java
@Transactional
public buyProducts(long productId, int num) {
    ...
    if (store < num) {
        // 库存不够，购买失败:
        throw new IllegalArgumentException("No enough products");
    }
    ...
}
```
如果要针对Checked Exception回滚事务，需要在@Transactional注解中写出来：
```java
@Transactional(rollbackFor = {RuntimeException.class, IOException.class})
public buyProducts(long productId, int num) throws IOException {
    ...
}
```
上述代码表示在抛出RuntimeException或IOException时，事务将回滚。

为了简化代码，我们强烈建议业务异常体系从RuntimeException派生，这样就不必声明任何特殊异常即可让Spring的声明式事务正常工作：
```java
public class BusinessException extends RuntimeException {
    ...
}

public class LoginException extends BusinessException {
    ...
}

public class PaymentException extends BusinessException {
    ...
}
```

#### 事务边界
在使用事务的时候，明确事务边界非常重要。对于声明式事务，例如，下面的register()方法：
```java
@Component
public class UserService {
    @Transactional
    public User register(String email, String password, String name) { // 事务开始
       ...
    } // 事务结束
}
```
它的事务边界就是register()方法开始和结束。

类似的，一个负责给用户增加积分的addBonus()方法：
```java
@Component
public class BonusService {
    @Transactional
    public void addBonus(long userId, int bonus) { // 事务开始
       ...
    } // 事务结束
}
```
它的事务边界就是addBonus()方法开始和结束。

在现实世界中，问题总是要复杂一点点。用户注册后，能自动获得100积分，因此，实际代码如下：
```java
@Component
public class UserService {
    @Autowired
    BonusService bonusService;

    @Transactional
    public User register(String email, String password, String name) {
        // 插入用户记录:
        User user = jdbcTemplate.insert("...");
        // 增加100积分:
        bonusService.addBonus(user.id, 100);
    }
}
```
现在问题来了：调用方（比如RegisterController）调用UserService.register()这个事务方法，它在内部又调用了BonusService.addBonus()这个事务方法，一共有几个事务？如果addBonus()抛出了异常需要回滚事务，register()方法的事务是否也要回滚？

#### 事务传播
要解决上面的问题，我们首先要定义事务的传播模型。

假设用户注册的入口是RegisterController，它本身没有事务，仅仅是调用UserService.register()这个事务方法：
```java
@Controller
public class RegisterController {
    @Autowired
    UserService userService;

    @PostMapping("/register")
    public ModelAndView doRegister(HttpServletRequest req) {
        String email = req.getParameter("email");
        String password = req.getParameter("password");
        String name = req.getParameter("name");
        User user = userService.register(email, password, name);
        return ...
    }
}
```
因此，UserService.register()这个事务方法的起始和结束，就是事务的范围。

我们需要关心的问题是，在UserService.register()这个事务方法内，调用BonusService.addBonus()，我们期待的事务行为是什么：
```java
@Transactional
public User register(String email, String password, String name) {
    // 事务已开启:
    User user = jdbcTemplate.insert("...");
    // ???:
    bonusService.addBonus(user.id, 100);
} // 事务结束
```
对于大多数业务来说，我们期待BonusService.addBonus()的调用，和UserService.register()应当融合在一起，它的行为应该如下：

UserService.register()已经开启了一个事务，那么在内部调用BonusService.addBonus()时，BonusService.addBonus()方法就没必要再开启一个新事务，直接加入到BonusService.register()的事务里就好了。

其实就相当于：

1. UserService.register()先执行了一条INSERT语句：INSERT INTO users ...
2. BonusService.addBonus()再执行一条INSERT语句：INSERT INTO bonus ...

因此，Spring的声明式事务为事务传播定义了几个级别，默认传播级别就是REQUIRED，它的意思是，如果当前没有事务，就创建一个新事务，如果当前有事务，就加入到当前事务中执行。

我们观察UserService.register()方法，它在RegisterController中执行，因为RegisterController没有事务，因此，UserService.register()方法会自动创建一个新事务。

在UserService.register()方法内部，调用BonusService.addBonus()方法时，因为BonusService.addBonus()检测到当前已经有事务了，因此，它会加入到当前事务中执行。

因此，整个业务流程的事务边界就清晰了：它只有一个事务，并且范围就是UserService.register()方法。

有的童鞋会问：把BonusService.addBonus()方法的@Transactional去掉，变成一个普通方法，那不就规避了复杂的传播模型吗？

去掉BonusService.addBonus()方法的@Transactional，会引来另一个问题，即其他地方如果调用BonusService.addBonus()方法，那就没法保证事务了。例如，规定用户登录时积分+5：
```java
@Controller
public class LoginController {
    @Autowired
    BonusService bonusService;

    @PostMapping("/login")
    public ModelAndView doLogin(HttpServletRequest req) {
        User user = ...
        bonusService.addBonus(user.id, 5);
    }
}
```
可见，BonusService.addBonus()方法必须要有@Transactional，否则，登录后积分就无法添加了。

默认的事务传播级别是REQUIRED，它满足绝大部分的需求。还有一些其他的传播级别：

- SUPPORTS：表示如果有事务，就加入到当前事务，如果没有，那也不开启事务执行。这种传播级别可用于查询方法，因为SELECT语句既可以在事务内执行，也可以不需要事务；
- MANDATORY：表示必须要存在当前事务并加入执行，否则将抛出异常。这种传播级别可用于核心更新逻辑，比如用户余额变更，它总是被其他事务方法调用，不能直接由非事务方法调用；
- REQUIRES_NEW：表示不管当前有没有事务，都必须开启一个新的事务执行。如果当前已经有事务，那么当前事务会挂起，等新事务完成后，再恢复执行；
- NOT_SUPPORTED：表示不支持事务，如果当前有事务，那么当前事务会挂起，等这个方法执行完成后，再恢复执行；
- NEVER：和NOT_SUPPORTED相比，它不但不支持事务，而且在监测到当前有事务时，会抛出异常拒绝执行；
- NESTED：表示如果当前有事务，则开启一个嵌套级别事务，如果当前没有事务，则开启一个新事务。

上面这么多种事务的传播级别，其实默认的REQUIRED已经满足绝大部分需求，SUPPORTS和REQUIRES_NEW在少数情况下会用到，其他基本不会用到，因为把事务搞得越复杂，不仅逻辑跟着复杂，而且速度也会越慢。

定义事务的传播级别也是写在@Transactional注解里的：
```java
@Transactional(propagation = Propagation.REQUIRES_NEW)
public Product createProduct() {
    ...
}
```
现在只剩最后一个问题了：Spring是如何传播事务的？

我们在JDBC中使用事务的时候，是这么个写法：
```java
Connection conn = openConnection();
try {
    // 关闭自动提交:
    conn.setAutoCommit(false);
    // 执行多条SQL语句:
    insert(); update(); delete();
    // 提交事务:
    conn.commit();
} catch (SQLException e) {
    // 回滚事务:
    conn.rollback();
} finally {
    conn.setAutoCommit(true);
    conn.close();
}
```
Spring使用声明式事务，最终也是通过执行JDBC事务来实现功能的，那么，一个事务方法，如何获知当前是否存在事务？

答案是使用ThreadLocal。Spring总是把JDBC相关的Connection和TransactionStatus实例绑定到ThreadLocal。如果一个事务方法从ThreadLocal未取到事务，那么它会打开一个新的JDBC连接，同时开启一个新的事务，否则，它就直接使用从ThreadLocal获取的JDBC连接以及TransactionStatus。

因此，事务能正确传播的前提是，方法调用是在一个线程内才行。如果像下面这样写：
```java
@Transactional
public User register(String email, String password, String name) { // BEGIN TX-A
    User user = jdbcTemplate.insert("...");
    new Thread(() -> {
        // BEGIN TX-B:
        bonusService.addBonus(user.id, 100);
        // END TX-B
    }).start();
} // END TX-A
```
在另一个线程中调用BonusService.addBonus()，它根本获取不到当前事务，因此，UserService.register()和BonusService.addBonus()两个方法，将分别开启两个完全独立的事务。

换句话说，事务只能在当前线程传播，无法跨线程传播。

那如果我们想实现跨线程传播事务呢？原理很简单，就是要想办法把当前线程绑定到ThreadLocal的Connection和TransactionStatus实例传递给新线程，但实现起来非常复杂，根据异常回滚更加复杂，不推荐自己去实现。


### 使用DAO
在传统的多层应用程序中，通常是Web层调用业务层，业务层调用数据访问层。业务层负责处理各种业务逻辑，而数据访问层只负责对数据进行增删改查。因此，实现数据访问层就是用JdbcTemplate实现对数据库的操作。

编写数据访问层的时候，可以使用DAO模式。DAO即Data Access Object的缩写，它没有什么神秘之处，实现起来基本如下：
```java
public class UserDao {

    @Autowired
    JdbcTemplate jdbcTemplate;

    User getById(long id) {
        ...
    }

    List<User> getUsers(int page) {
        ...
    }

    User createUser(User user) {
        ...
    }

    User updateUser(User user) {
        ...
    }

    void deleteUser(User user) {
        ...
    }
}
```
Spring提供了一个JdbcDaoSupport类，用于简化DAO的实现。这个JdbcDaoSupport没什么复杂的，核心代码就是持有一个JdbcTemplate：
```java
public abstract class JdbcDaoSupport extends DaoSupport {

    private JdbcTemplate jdbcTemplate;

    public final void setJdbcTemplate(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
        initTemplateConfig();
    }

    public final JdbcTemplate getJdbcTemplate() {
        return this.jdbcTemplate;
    }

    ...
}
```
它的意图是子类直接从JdbcDaoSupport继承后，可以随时调用getJdbcTemplate()获得JdbcTemplate的实例。那么问题来了：因为JdbcDaoSupport的jdbcTemplate字段没有标记@Autowired，所以，子类想要注入JdbcTemplate，还得自己想个办法：
```java
@Component
@Transactional
public class UserDao extends JdbcDaoSupport {
    @Autowired
    JdbcTemplate jdbcTemplate;

    @PostConstruct
    public void init() {
        super.setJdbcTemplate(jdbcTemplate);
    }
}
```
那既然UserDao都已经注入了JdbcTemplate，那再把它放到父类里，通过getJdbcTemplate()访问岂不是多此一举？

如果使用传统的XML配置，并不需要编写@Autowired JdbcTemplate jdbcTemplate，但是考虑到现在基本上是使用注解的方式，我们可以编写一个AbstractDao，专门负责注入JdbcTemplate：
```java
public abstract class AbstractDao extends JdbcDaoSupport {
    @Autowired
    private JdbcTemplate jdbcTemplate;

    @PostConstruct
    public void init() {
        super.setJdbcTemplate(jdbcTemplate);
    }
}
```
这样，子类的代码就非常干净，可以直接调用getJdbcTemplate()：
```java
@Component
@Transactional
public class UserDao extends AbstractDao {
    public User getById(long id) {
        return getJdbcTemplate().queryForObject(
                "SELECT * FROM users WHERE id = ?",
                new BeanPropertyRowMapper<>(User.class),
                id
        );
    }
    ...
}
```
倘若肯再多写一点样板代码，就可以把AbstractDao改成泛型，并实现getById()，getAll()，deleteById()这样的通用方法：
```java
public abstract class AbstractDao<T> extends JdbcDaoSupport {
    private String table;
    private Class<T> entityClass;
    private RowMapper<T> rowMapper;

    public AbstractDao() {
        // 获取当前类型的泛型类型:
        this.entityClass = getParameterizedType();
        this.table = this.entityClass.getSimpleName().toLowerCase() + "s";
        this.rowMapper = new BeanPropertyRowMapper<>(entityClass);
    }

    public T getById(long id) {
        return getJdbcTemplate().queryForObject("SELECT * FROM " + table + " WHERE id = ?", this.rowMapper, id);
    }

    public List<T> getAll(int pageIndex) {
        int limit = 100;
        int offset = limit * (pageIndex - 1);
        return getJdbcTemplate().query("SELECT * FROM " + table + " LIMIT ? OFFSET ?",
                new Object[] { limit, offset },
                this.rowMapper);
    }

    public void deleteById(long id) {
        getJdbcTemplate().update("DELETE FROM " + table + " WHERE id = ?", id);
    }
    ...
}
```
这样，每个子类就自动获得了这些通用方法：
```java
@Component
@Transactional
public class UserDao extends AbstractDao<User> {
    // 已经有了:
    // User getById(long)
    // List<User> getAll(int)
    // void deleteById(long)
}

@Component
@Transactional
public class BookDao extends AbstractDao<Book> {
    // 已经有了:
    // Book getById(long)
    // List<Book> getAll(int)
    // void deleteById(long)
}
```
可见，DAO模式就是一个简单的数据访问模式，是否使用DAO，根据实际情况决定，因为很多时候，直接在Service层操作数据库也是完全没有问题的。


### 集成Hibernate
使用JdbcTemplate的时候，我们用得最多的方法就是List<T> query(String sql, Object[] args, RowMapper rowMapper)。这个RowMapper的作用就是把ResultSet的一行记录映射为Java Bean。

这种把关系数据库的表记录映射为Java对象的过程就是ORM：Object-Relational Mapping。ORM既可以把记录转换成Java对象，也可以把Java对象转换为行记录。

使用JdbcTemplate配合RowMapper可以看作是最原始的ORM。如果要实现更自动化的ORM，可以选择成熟的ORM框架，例如Hibernate。

我们来看看如何在Spring中集成Hibernate。

Hibernate作为ORM框架，它可以替代JdbcTemplate，但Hibernate仍然需要JDBC驱动，所以，我们需要引入JDBC驱动、连接池，以及Hibernate本身。在Maven中，我们加入以下依赖项：
```xml
<!-- JDBC驱动，这里使用HSQLDB -->
<dependency>
    <groupId>org.hsqldb</groupId>
    <artifactId>hsqldb</artifactId>
    <version>2.5.0</version>
</dependency>

<!-- JDBC连接池 -->
<dependency>
    <groupId>com.zaxxer</groupId>
    <artifactId>HikariCP</artifactId>
    <version>3.4.2</version>
</dependency>

<!-- Hibernate -->
<dependency>
    <groupId>org.hibernate</groupId>
    <artifactId>hibernate-core</artifactId>
    <version>5.4.2.Final</version>
</dependency>

<!-- Spring Context和Spring ORM -->
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-context</artifactId>
    <version>5.2.0.RELEASE</version>
</dependency>
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-orm</artifactId>
    <version>5.2.0.RELEASE</version>
</dependency>
```
在AppConfig中，我们仍然需要创建DataSource、引入JDBC配置文件，以及启用声明式事务：
```java
@Configuration
@ComponentScan
@EnableTransactionManagement
@PropertySource("jdbc.properties")
public class AppConfig {
    @Bean
    DataSource createDataSource() {
        ...
    }
}
```
为了启用Hibernate，我们需要创建一个LocalSessionFactoryBean：
```java
public class AppConfig {
    @Bean
    LocalSessionFactoryBean createSessionFactory(@Autowired DataSource dataSource) {
        var props = new Properties();
        props.setProperty("hibernate.hbm2ddl.auto", "update"); // 生产环境不要使用
        props.setProperty("hibernate.dialect", "org.hibernate.dialect.HSQLDialect");
        props.setProperty("hibernate.show_sql", "true");
        var sessionFactoryBean = new LocalSessionFactoryBean();
        sessionFactoryBean.setDataSource(dataSource);
        // 扫描指定的package获取所有entity class:
        sessionFactoryBean.setPackagesToScan("com.itranswarp.learnjava.entity");
        sessionFactoryBean.setHibernateProperties(props);
        return sessionFactoryBean;
    }
}
```
注意我们在定制Bean中讲到过FactoryBean，LocalSessionFactoryBean是一个FactoryBean，它会再自动创建一个SessionFactory，在Hibernate中，Session是封装了一个JDBC Connection的实例，而SessionFactory是封装了JDBC DataSource的实例，即SessionFactory持有连接池，每次需要操作数据库的时候，SessionFactory创建一个新的Session，相当于从连接池获取到一个新的Connection。SessionFactory就是Hibernate提供的最核心的一个对象，但LocalSessionFactoryBean是Spring提供的为了让我们方便创建SessionFactory的类。

注意到上面创建LocalSessionFactoryBean的代码，首先用Properties持有Hibernate初始化SessionFactory时用到的所有设置，常用的设置请参考Hibernate文档，这里我们只定义了3个设置：

- hibernate.hbm2ddl.auto=update：表示自动创建数据库的表结构，注意不要在生产环境中启用；
- hibernate.dialect=org.hibernate.dialect.HSQLDialect：指示Hibernate使用的数据库是HSQLDB。Hibernate使用一种HQL的查询语句，它和SQL类似，但真正在“翻译”成SQL时，会根据设定的数据库“方言”来生成针对数据库优化的SQL；
- hibernate.show_sql=true：让Hibernate打印执行的SQL，这对于调试非常有用，我们可以方便地看到Hibernate生成的SQL语句是否符合我们的预期。

除了设置DataSource和Properties之外，注意到setPackagesToScan()我们传入了一个package名称，它指示Hibernate扫描这个包下面的所有Java类，自动找出能映射为数据库表记录的JavaBean。后面我们会仔细讨论如何编写符合Hibernate要求的JavaBean。

紧接着，我们还需要创建HibernateTemplate以及HibernateTransactionManager：
```java
public class AppConfig {
    @Bean
    HibernateTemplate createHibernateTemplate(@Autowired SessionFactory sessionFactory) {
        return new HibernateTemplate(sessionFactory);
    }

    @Bean
    PlatformTransactionManager createTxManager(@Autowired SessionFactory sessionFactory) {
        return new HibernateTransactionManager(sessionFactory);
    }
}
```
这两个Bean的创建都十分简单。HibernateTransactionManager是配合Hibernate使用声明式事务所必须的，而HibernateTemplate则是Spring为了便于我们使用Hibernate提供的工具类，不是非用不可，但推荐使用以简化代码。

到此为止，所有的配置都定义完毕，我们来看看如何将数据库表结构映射为Java对象。

考察如下的数据库表：
```sql
CREATE TABLE user
    id BIGINT NOT NULL AUTO_INCREMENT,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    createdAt BIGINT NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `email` (`email`)
);
```
其中，id是自增主键，email、password、name是VARCHAR类型，email带唯一索引以确保唯一性，createdAt存储整型类型的时间戳。用JavaBean表示如下：
```java
public class User {
    private Long id;
    private String email;
    private String password;
    private String name;
    private Long createdAt;

    // getters and setters
    ...
}
```
这种映射关系十分易懂，但我们需要添加一些注解来告诉Hibernate如何把User类映射到表记录：
```java
@Entity
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(nullable = false, updatable = false)
    public Long getId() { ... }

    @Column(nullable = false, unique = true, length = 100)
    public String getEmail() { ... }

    @Column(nullable = false, length = 100)
    public String getPassword() { ... }

    @Column(nullable = false, length = 100)
    public String getName() { ... }

    @Column(nullable = false, updatable = false)
    public Long getCreatedAt() { ... }
}
```
如果一个JavaBean被用于映射，我们就标记一个@Entity。默认情况下，映射的表名是user，如果实际的表名不同，例如实际表名是users，可以追加一个@Table(name="users")表示：
```java
@Entity
@Table(name="users)
public class User {
    ...
}
```
每个属性到数据库列的映射用@Column()标识，nullable指示列是否允许为NULL，updatable指示该列是否允许被用在UPDATE语句，length指示String类型的列的长度（如果没有指定，默认是255）。

对于主键，还需要用@Id标识，自增主键再追加一个@GeneratedValue，以便Hibernate能读取到自增主键的值。

主键id定义的类型不是long，而是Long。这是因为Hibernate如果检测到主键为null，就不会在INSERT语句中指定主键的值，而是返回由数据库生成的自增值，否则，Hibernate认为我们的程序指定了主键的值，会在INSERT语句中直接列出。long型字段总是具有默认值0，因此，每次插入的主键值总是0，导致除第一次外后续插入都将失败。

createdAt虽然是整型，但我们并没有使用long，而是Long，这是因为使用基本类型会导致某种查询会添加意外的条件，后面我们会详细讨论，这里只需牢记，作为映射使用的JavaBean，所有属性都使用包装类型而不是基本类型。

使用Hibernate时，不要使用基本类型的属性，总是使用包装类型，如Long或Integer。

类似的，我们再定义一个Book类：
```java
@Entity
public class Book {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(nullable = false, updatable = false)
    public Long getId() { ... }

    @Column(nullable = false, length = 100)
    public String getTitle() { ... }

    @Column(nullable = false, updatable = false)
    public Long getCreatedAt() { ... }
}
```
如果仔细观察User和Book，会发现它们定义的id、createdAt属性是一样的，这在数据库表结构的设计中很常见：对于每个表，通常我们会统一使用一种主键生成机制，并添加createdAt表示创建时间，updatedAt表示修改时间等通用字段。

不必在User和Book中重复定义这些通用字段，我们可以把它们提到一个抽象类中：
```java
@MappedSuperclass
public abstract class AbstractEntity {

    private Long id;
    private Long createdAt;

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(nullable = false, updatable = false)
    public Long getId() { ... }

    @Column(nullable = false, updatable = false)
    public Long getCreatedAt() { ... }

    @Transient
    public ZonedDateTime getCreatedDateTime() {
        return Instant.ofEpochMilli(this.createdAt).atZone(ZoneId.systemDefault());
    }

    @PrePersist
    public void preInsert() {
        setCreatedAt(System.currentTimeMillis());
    }
}
```
对于AbstractEntity来说，我们要标注一个@MappedSuperclass表示它用于继承。此外，注意到我们定义了一个@Transient方法，它返回一个“虚拟”的属性。因为getCreatedDateTime()是计算得出的属性，而不是从数据库表读出的值，因此必须要标注@Transient，否则Hibernate会尝试从数据库读取名为createdDateTime这个不存在的字段从而出错。

再注意到@PrePersist标识的方法，它表示在我们将一个JavaBean持久化到数据库之前（即执行INSERT语句），Hibernate会先执行该方法，这样我们就可以自动设置好createdAt属性。

有了AbstractEntity，我们就可以大幅简化User和Book：
```java
@Entity
public class User extends AbstractEntity {

    @Column(nullable = false, unique = true, length = 100)
    public String getEmail() { ... }

    @Column(nullable = false, length = 100)
    public String getPassword() { ... }

    @Column(nullable = false, length = 100)
    public String getName() { ... }
}
```
注意到使用的所有注解均来自javax.persistence，它是JPA规范的一部分。这里我们只介绍使用注解的方式配置Hibernate映射关系，不再介绍传统的比较繁琐的XML配置。通过Spring集成Hibernate时，也不再需要hibernate.cfg.xml配置文件，用一句话总结：

使用Spring集成Hibernate，配合JPA注解，无需任何额外的XML配置。

类似User、Book这样的用于ORM的Java Bean，我们通常称之为Entity Bean。

最后，我们来看看如果对user表进行增删改查。因为使用了Hibernate，因此，我们要做的，实际上是对User这个JavaBean进行“增删改查”。我们编写一个UserService，注入HibernateTemplate以便简化代码：
```java
@Component
@Transactional
public class UserService {
    @Autowired
    HibernateTemplate hibernateTemplate;
}
```

#### Insert操作
要持久化一个User实例，我们只需调用save()方法。以register()方法为例，代码如下：
```java
public User register(String email, String password, String name) {
    // 创建一个User对象:
    User user = new User();
    // 设置好各个属性:
    user.setEmail(email);
    user.setPassword(password);
    user.setName(name);
    // 不要设置id，因为使用了自增主键
    // 保存到数据库:
    hibernateTemplate.save(user);
    // 现在已经自动获得了id:
    System.out.println(user.getId());
    return user;
}
```

#### Delete操作
删除一个User相当于从表中删除对应的记录。注意Hibernate总是用id来删除记录，因此，要正确设置User的id属性才能正常删除记录：
```java
public boolean deleteUser(Long id) {
    User user = hibernateTemplate.get(User.class, id);
    if (user != null) {
        hibernateTemplate.delete(user);
        return true;
    }
    return false;
}
```
通过主键删除记录时，一个常见的用法是先根据主键加载该记录，再删除。load()和get()都可以根据主键加载记录，它们的区别在于，当记录不存在时，get()返回null，而load()抛出异常。

#### Update操作
更新记录相当于先更新User的指定属性，然后调用update()方法：
```java
public void updateUser(Long id, String name) {
    User user = hibernateTemplate.load(User.class, id);
    user.setName(name);
    hibernateTemplate.update(user);
}
```
前面我们在定义User时，对有的属性标注了@Column(updatable=false)。Hibernate在更新记录时，它只会把@Column(updatable=true)的属性加入到UPDATE语句中，这样可以提供一层额外的安全性，即如果不小心修改了User的email、createdAt等属性，执行update()时并不会更新对应的数据库列。但也必须牢记：这个功能是Hibernate提供的，如果绕过Hibernate直接通过JDBC执行UPDATE语句仍然可以更新数据库的任意列的值。

最后，我们编写的大部分方法都是各种各样的查询。根据id查询我们可以直接调用load()或get()，如果要使用条件查询，有3种方法。

假设我们想执行以下查询：
```sql
SELECT * FROM user WHERE email = ? AND password = ?
```
我们来看看可以使用什么查询。

#### 使用Example查询
第一种方法是使用findByExample()，给出一个User实例，Hibernate把该实例所有非null的属性拼成WHERE条件：
```java
public User login(String email, String password) {
    User example = new User();
    example.setEmail(email);
    example.setPassword(password);
    List<User> list = hibernateTemplate.findByExample(example);
    return list.isEmpty() ? null : list.get(0);
}
```
因为example实例只有email和password两个属性为非null，所以最终生成的WHERE语句就是WHERE email = ? AND password = ?。

如果我们把User的createdAt的类型从Long改为long，findByExample()的查询将出问题，原因在于example实例的long类型字段有了默认值0，导致Hibernate最终生成的WHERE语句意外变成了WHERE email = ? AND password = ? AND createdAt = 0。显然，额外的查询条件将导致错误的查询结果。

使用findByExample()时，注意基本类型字段总是会加入到WHERE条件！

#### 使用Criteria查询
第二种查询方法是使用Criteria查询，可以实现如下：
```java
public User login(String email, String password) {
    DetachedCriteria criteria = DetachedCriteria.forClass(User.class);
    criteria.add(Restrictions.eq("email", email))
            .add(Restrictions.eq("password", password));
    List<User> list = (List<User>) hibernateTemplate.findByCriteria(criteria);
    return list.isEmpty() ? null : list.get(0);
}
```
DetachedCriteria使用链式语句来添加多个AND条件。和findByExample()相比，findByCriteria()可以组装出更灵活的WHERE条件，例如：
```sql
SELECT * FROM user WHERE (email = ? OR name = ?) AND password = ?
```
上述查询没法用findByExample()实现，但用Criteria查询可以实现如下：
```java
DetachedCriteria criteria = DetachedCriteria.forClass(User.class);
criteria.add(
    Restrictions.and(
        Restrictions.or(
            Restrictions.eq("email", email),
            Restrictions.eq("name", email)
        ),
        Restrictions.eq("password", password)
    )
);
```
只要组织好Restrictions的嵌套关系，Criteria查询可以实现任意复杂的查询。

#### 使用HQL查询
最后一种常用的查询是直接编写Hibernate内置的HQL查询：
```java
List<User> list = (List<User>) hibernateTemplate.find("FROM User WHERE email=? AND password=?", email, password);
```
和SQL相比，HQL使用类名和属性名，由Hibernate自动转换为实际的表名和列名。详细的HQL语法可以参考Hibernate文档。

除了可以直接传入HQL字符串外，Hibernate还可以使用一种NamedQuery，它给查询起个名字，然后保存在注解中。使用NamedQuery时，我们要先在User类标注：
```java
@NamedQueries(
    @NamedQuery(
        // 查询名称:
        name = "login",
        // 查询语句:
        query = "SELECT u FROM User u WHERE u.email=?0 AND u.password=?1"
    )
)
@Entity
public class User extends AbstractEntity {
    ...
}
```
注意到引入的NamedQuery是javax.persistence.NamedQuery，它和直接传入HQL有点不同的是，占位符使用?0、?1，并且索引是从0开始的（真乱）。

使用NamedQuery只需要引入查询名和参数：
```java
public User login(String email, String password) {
    List<User> list = (List<User>) hibernateTemplate.findByNamedQuery("login", email, password);
    return list.isEmpty() ? null : list.get(0);
}
```
直接写HQL和使用NamedQuery各有优劣。前者可以在代码中直观地看到查询语句，后者可以在User类统一管理所有相关查询。

#### 使用Hibernate原生接口
如果要使用Hibernate原生接口，但不知道怎么写，可以参考HibernateTemplate的源码。使用Hibernate的原生接口实际上总是从SessionFactory出发，它通常用全局变量存储，在HibernateTemplate中以成员变量被注入。有了SessionFactory，使用Hibernate用法如下：
```java
void operation() {
    Session session = null;
    boolean isNew = false;
    // 获取当前Session或者打开新的Session:
    try {
        session = this.sessionFactory.getCurrentSession();
    } catch (HibernateException e) {
        session = this.sessionFactory.openSession();
        isNew = true;
    }
    // 操作Session:
    try {
        User user = session.load(User.class, 123L);
    }
    finally {
        // 关闭新打开的Session:
        if (isNew) {
            session.close();
        }
    }
}
```

### 集成JPA
JavaEE早在1999年就发布了，并且有Servlet、JMS等诸多标准。和其他平台不同，Java世界早期非常热衷于标准先行，各家跟进：大家先坐下来把接口定了，然后，各自回家干活去实现接口，这样，用户就可以在不同的厂家提供的产品进行选择，还可以随意切换，因为用户编写代码的时候只需要引用接口，并不需要引用具体的底层实现（想想JDBC）。

JPA（Java Persistence API）就是JavaEE的一个ORM标准，它的实现其实和Hibernate没啥本质区别，但是用户如果使用JPA，那么引用的就是javax.persistence这个“标准”包，而不是org.hibernate这样的第三方包。因为JPA只是接口，所以，还需要选择一个实现产品，跟JDBC接口和MySQL驱动一个道理。

我们使用JPA时也完全可以选择Hibernate作为底层实现，但也可以选择其它的JPA提供方，比如EclipseLink。Spring内置了JPA的集成，并支持选择Hibernate或EclipseLink作为实现。这里我们仍然以主流的Hibernate作为JPA实现为例子，演示JPA的基本用法。

和使用Hibernate一样，我们只需要引入如下依赖：
```
org.springframework:spring-context:5.2.0.RELEASE
org.springframework:spring-orm:5.2.0.RELEASE
javax.annotation:javax.annotation-api:1.3.2
org.hibernate:hibernate-core:5.4.2.Final
com.zaxxer:HikariCP:3.4.2
org.hsqldb:hsqldb:2.5.0
```
然后，在AppConfig中启用声明式事务管理，创建DataSource：
```java
@Configuration
@ComponentScan
@EnableTransactionManagement
@PropertySource("jdbc.properties")
public class AppConfig {
    @Bean
    DataSource createDataSource() { ... }
}
```
使用Hibernate时，我们需要创建一个LocalSessionFactoryBean，并让它再自动创建一个SessionFactory。使用JPA也是类似的，我们需要创建一个LocalContainerEntityManagerFactoryBean，并让它再自动创建一个EntityManagerFactory：
```java
@Bean
LocalContainerEntityManagerFactoryBean createEntityManagerFactory(@Autowired DataSource dataSource) {
    var entityManagerFactoryBean = new LocalContainerEntityManagerFactoryBean();
    // 设置DataSource:
    entityManagerFactoryBean.setDataSource(dataSource);
    // 扫描指定的package获取所有entity class:
    entityManagerFactoryBean.setPackagesToScan("com.itranswarp.learnjava.entity");
    // 指定JPA的提供商是Hibernate:
    JpaVendorAdapter vendorAdapter = new HibernateJpaVendorAdapter();
    entityManagerFactoryBean.setJpaVendorAdapter(vendorAdapter);
    // 设定特定提供商自己的配置:
    var props = new Properties();
    props.setProperty("hibernate.hbm2ddl.auto", "update");
    props.setProperty("hibernate.dialect", "org.hibernate.dialect.HSQLDialect");
    props.setProperty("hibernate.show_sql", "true");
    entityManagerFactoryBean.setJpaProperties(props);
    return entityManagerFactoryBean;
}
```
观察上述代码，除了需要注入DataSource和设定自动扫描的package外，还需要指定JPA的提供商，这里使用Spring提供的一个HibernateJpaVendorAdapter，最后，针对Hibernate自己需要的配置，以Properties的形式注入。

最后，我们还需要实例化一个JpaTransactionManager，以实现声明式事务：
```java
@Bean
PlatformTransactionManager createTxManager(@Autowired EntityManagerFactory entityManagerFactory) {
    return new JpaTransactionManager(entityManagerFactory);
}
```
这样，我们就完成了JPA的全部初始化工作。使用Spring+Hibernate作为JPA实现，无需任何配置文件。

所有Entity Bean的配置和上一节完全相同，全部采用Annotation标注。我们现在只需关心具体的业务类如何通过JPA接口操作数据库。

还是以UserService为例，除了标注@Component和@Transactional外，我们需要注入一个EntityManager，但是不要使用Autowired，而是@PersistenceContext：
```java
@Component
@Transactional
public class UserService {
    @PersistenceContext
    EntityManager em;
}
```
我们回顾一下JDBC、Hibernate和JPA提供的接口，实际上，它们的关系如下：

JDBC       |   Hibernate    |  JPA
---------- | -------------- | --------------------
DataSource | SessionFactory | EntityManagerFactory
Connection | Session        | EntityManager

SessionFactory和EntityManagerFactory相当于DataSource，Session和EntityManager相当于Connection。每次需要访问数据库的时候，需要获取新的Session和EntityManager，用完后再关闭。

但是，注意到UserService注入的不是EntityManagerFactory，而是EntityManager，并且标注了@PersistenceContext。难道使用JPA可以允许多线程操作同一个EntityManager？

实际上这里注入的并不是真正的EntityManager，而是一个EntityManager的代理类，相当于：
```java
public class EntityManagerProxy implements EntityManager {
    private EntityManagerFactory emf;
}
```
Spring遇到标注了@PersistenceContext的EntityManager会自动注入代理，该代理会在必要的时候自动打开EntityManager。换句话说，多线程引用的EntityManager虽然是同一个代理类，但该代理类内部针对不同线程会创建不同的EntityManager实例。

简单总结一下，标注了@PersistenceContext的EntityManager可以被多线程安全地共享。

因此，在UserService的每个业务方法里，直接使用EntityManager就很方便。以主键查询为例：
```java
public User getUserById(long id) {
    User user = this.em.find(User.class, id);
    if (user == null) {
        throw new RuntimeException("User not found by id: " + id);
    }
    return user;
}
```
JPA同样支持Criteria查询，比如我们需要的查询如下：
```sql
SELECT * FROM user WHERE email = ?
```
使用Criteria查询的代码如下：
```java
public User fetchUserByEmail(String email) {
    // CriteriaBuilder:
    var cb = em.getCriteriaBuilder();
    CriteriaQuery<User> q = cb.createQuery(User.class);
    Root<User> r = q.from(User.class);
    q.where(cb.equal(r.get("email"), cb.parameter(String.class, "e")));
    TypedQuery<User> query = em.createQuery(q);
    // 绑定参数:
    query.setParameter("e", email);
    // 执行查询:
    List<User> list = query.getResultList();
    return list.isEmpty() ? null : list.get(0);
}
```
一个简单的查询用Criteria写出来就像上面那样复杂，太恐怖了，如果条件多加几个，这种写法谁读得懂？

所以，正常人还是建议写JPQL查询，它的语法和HQL基本差不多：
```java
public User getUserByEmail(String email) {
    // JPQL查询:
    TypedQuery<User> query = em.createQuery("SELECT u FROM User u WHERE u.email = :e", User.class);
    query.setParameter("e", email);
    List<User> list = query.getResultList();
    if (list.isEmpty()) {
        throw new RuntimeException("User not found by email.");
    }
    return list.get(0);
}
```
同样的，JPA也支持NamedQuery，即先给查询起个名字，再按名字创建查询：
```java
public User login(String email, String password) {
    TypedQuery<User> query = em.createNamedQuery("login", User.class);
    query.setParameter("e", email);
    query.setParameter("p", password);
    List<User> list = query.getResultList();
    return list.isEmpty() ? null : list.get(0);
}
```
NamedQuery通过注解标注在User类上，它的定义和上一节的User类一样：
```java
@NamedQueries(
    @NamedQuery(
        name = "login",
        query = "SELECT u FROM User u WHERE u.email=:e AND u.password=:p"
    )
)
@Entity
public class User {
    ...
}
```
对数据库进行增删改的操作，可以分别使用persist()、remove()和merge()方法，参数均为Entity Bean本身，使用非常简单，这里不再多述。





### 集成MyBatis

### 设计ORM




## 开发Web应用
在Web开发一章中，我们已经详细介绍了JavaEE中Web开发的基础：Servlet。具体地说，有以下几点：

- Servlet规范定义了几种标准组件：Servlet、JSP、Filter和Listener；
- Servlet的标准组件总是运行在Servlet容器中，如Tomcat、Jetty、WebLogic等。

直接使用Servlet进行Web开发好比直接在JDBC上操作数据库，比较繁琐，更好的方法是在Servlet基础上封装MVC框架，基于MVC开发Web应用，大部分时候，不需要接触Servlet API，开发省时省力。

常用的MVC框架有：

- Struts：最古老的一个MVC框架，目前版本是2，和1.x有很大的区别；
- WebWork：一个比Struts设计更优秀的MVC框架，但不知道出于什么原因，从2.0开始把自己的代码全部塞给Struts 2了；
- Turbine：一个重度使用Velocity，强调布局的MVC框架；

Spring虽然都可以集成任何Web框架，但是，Spring本身也开发了一个MVC框架，就叫Spring MVC。这个MVC框架设计得足够优秀以至于我们已经不想再费劲去集成类似Struts这样的框架了。

### 使用Spring MVC
我们在前面介绍Web开发时已经讲过了Java Web的基础：Servlet容器，以及标准的Servlet组件：

- Servlet：能处理HTTP请求并将HTTP响应返回；
- JSP：一种嵌套Java代码的HTML，将被编译为Servlet；
- Filter：能过滤指定的URL以实现拦截功能；
- Listener：监听指定的事件，如ServletContext、HttpSession的创建和销毁。

此外，Servlet容器为每个Web应用程序自动创建一个唯一的ServletContext实例，这个实例就代表了Web应用程序本身。

如果直接使用Spring MVC，我们写出来的代码类似：
```java
@Controller
public class UserController {
    @GetMapping("/register")
    public ModelAndView register() {
        ...
    }

    @PostMapping("/signin")
    public ModelAndView signin(@RequestParam("email") String email, @RequestParam("password") String password) {
        ...
    }
    ...
}
```
但是，Spring提供的是一个IoC容器，所有的Bean，包括Controller，都在Spring IoC容器中被初始化，而Servlet容器由JavaEE服务器提供（如Tomcat），Servlet容器对Spring一无所知，他们之间到底依靠什么进行联系，又是以何种顺序初始化的？

这个标准的Maven Web工程目录结构如下：
```
spring-web-mvc
├── pom.xml
└── src
    └── main
        ├── java
        │   └── com
        │       └── itranswarp
        │           └── learnjava
        │               ├── AppConfig.java
        │               ├── DatabaseInitializer.java
        │               ├── entity
        │               │   └── User.java
        │               ├── service
        │               │   └── UserService.java
        │               └── web
        │                   └── UserController.java
        ├── resources
        │   ├── jdbc.properties
        │   └── logback.xml
        └── webapp
            ├── WEB-INF
            │   ├── templates
            │   │   ├── _base.html
            │   │   ├── index.html
            │   │   ├── profile.html
            │   │   ├── register.html
            │   │   └── signin.html
            │   └── web.xml
            └── static
                ├── css
                │   └── bootstrap.css
                └── js
                    └── jquery.js
```
其中，src/main/webapp是标准web目录，WEB-INF存放web.xml，编译的class，第三方jar，以及不允许浏览器直接访问的View模版，static目录存放所有静态文件。

在src/main/resources目录中存放的是Java程序读取的classpath资源文件，除了JDBC的配置文件jdbc.properties外，我们又新增了一个logback.xml，这是Logback的默认查找的配置文件：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <appender name="STDOUT"
        class="ch.qos.logback.core.ConsoleAppender">
        <layout class="ch.qos.logback.classic.PatternLayout">
            <Pattern>%d{yyyy-MM-dd HH:mm:ss} %-5level %logger{36} - %msg%n</Pattern>
        </layout>
    </appender>

    <logger name="com.itranswarp.learnjava" level="info" additivity="false">
        <appender-ref ref="STDOUT" />
    </logger>

    <root level="info">
        <appender-ref ref="STDOUT" />
    </root>
</configuration>
```
上面给出了一个写入到标准输出的Logback配置，可以基于上述配置添加写入到文件的配置。

在src/main/java中就是我们编写的Java代码了。

#### 配置Spring MVC
和普通Spring配置一样，我们编写正常的AppConfig后，只需加上@EnableWebMvc注解，就“激活”了Spring MVC：
```java
@Configuration
@ComponentScan
@EnableWebMvc // 启用Spring MVC
@EnableTransactionManagement
@PropertySource("classpath:/jdbc.properties")
public class AppConfig {
    ...
}
```
除了创建DataSource、JdbcTemplate、PlatformTransactionManager外，AppConfig需要额外创建几个用于Spring MVC的Bean：
```java
@Bean
WebMvcConfigurer createWebMvcConfigurer() {
    return new WebMvcConfigurer() {
        @Override
        public void addResourceHandlers(ResourceHandlerRegistry registry) {
            registry.addResourceHandler("/static/**").addResourceLocations("/static/");
        }
    };
}
```
WebMvcConfigurer并不是必须的，但我们在这里创建一个默认的WebMvcConfigurer，只覆写addResourceHandlers()，目的是让Spring MVC自动处理静态文件，并且映射路径为/static/**。

另一个必须要创建的Bean是ViewResolver，因为Spring MVC允许集成任何模板引擎，使用哪个模板引擎，就实例化一个对应的ViewResolver：
```java
@Bean
ViewResolver createViewResolver(@Autowired ServletContext servletContext) {
    PebbleEngine engine = new PebbleEngine.Builder().autoEscaping(true)
            .cacheActive(false)
            .loader(new ServletLoader(servletContext))
            .extension(new SpringExtension())
            .build();
    PebbleViewResolver viewResolver = new PebbleViewResolver();
    viewResolver.setPrefix("/WEB-INF/templates/");
    viewResolver.setSuffix("");
    viewResolver.setPebbleEngine(engine);
    return viewResolver;
}
```
ViewResolver通过指定prefix和suffix来确定如何查找View。上述配置使用Pebble引擎，指定模板文件存放在/WEB-INF/templates/目录下。

剩下的Bean都是普通的@Component，但Controller必须标记为@Controller，例如：
```java
// Controller使用@Controller标记而不是@Component:
@Controller
public class UserController {
    // 正常使用@Autowired注入:
    @Autowired
    UserService userService;

    // 处理一个URL映射:
    @GetMapping("/")
    public ModelAndView index() {
        ...
    }
    ...
}
```
如果是普通的Java应用程序，我们通过main()方法可以很简单地创建一个Spring容器的实例：
```java
public static void main(String[] args) {
    ApplicationContext context = new AnnotationConfigApplicationContext(AppConfig.class);
}
```
但是问题来了，现在是Web应用程序，而Web应用程序总是由Servlet容器创建，那么，Spring容器应该由谁创建？在什么时候创建？Spring容器中的Controller又是如何通过Servlet调用的？

在Web应用中启动Spring容器有很多种方法，可以通过Listener启动，也可以通过Servlet启动，可以使用XML配置，也可以使用注解配置。这里，我们只介绍一种最简单的启动Spring容器的方式。

第一步，我们在web.xml中配置Spring MVC提供的DispatcherServlet：
```xml
<!DOCTYPE web-app PUBLIC
 "-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN"
 "http://java.sun.com/dtd/web-app_2_3.dtd" >

<web-app>
    <servlet>
        <servlet-name>dispatcher</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <init-param>
            <param-name>contextClass</param-name>
            <param-value>org.springframework.web.context.support.AnnotationConfigWebApplicationContext</param-value>
        </init-param>
        <init-param>
            <param-name>contextConfigLocation</param-name>
            <param-value>com.itranswarp.learnjava.AppConfig</param-value>
        </init-param>
        <load-on-startup>0</load-on-startup>
    </servlet>

    <servlet-mapping>
        <servlet-name>dispatcher</servlet-name>
        <url-pattern>/*</url-pattern>
    </servlet-mapping>
</web-app>
```
初始化参数contextClass指定使用注解配置的AnnotationConfigWebApplicationContext，配置文件的位置参数contextConfigLocation指向AppConfig的完整类名，最后，把这个Servlet映射到/*，即处理所有URL。

上述配置可以看作一个样板配置，有了这个配置，Servlet容器会首先初始化Spring MVC的DispatcherServlet，在DispatcherServlet启动时，它根据配置AppConfig创建了一个类型是WebApplicationContext的IoC容器，完成所有Bean的初始化，并将容器绑到ServletContext上。

因为DispatcherServlet持有IoC容器，能从IoC容器中获取所有@Controller的Bean，因此，DispatcherServlet接收到所有HTTP请求后，根据Controller方法配置的路径，就可以正确地把请求转发到指定方法，并根据返回的ModelAndView决定如何渲染页面。

最后，我们在AppConfig中通过main()方法启动嵌入式Tomcat：
```java
public static void main(String[] args) throws Exception {
    Tomcat tomcat = new Tomcat();
    tomcat.setPort(Integer.getInteger("port", 8080));
    tomcat.getConnector();
    Context ctx = tomcat.addWebapp("", new File("src/main/webapp").getAbsolutePath());
    WebResourceRoot resources = new StandardRoot(ctx);
    resources.addPreResources(
            new DirResourceSet(resources, "/WEB-INF/classes", new File("target/classes").getAbsolutePath(), "/"));
    ctx.setResources(resources);
    tomcat.start();
    tomcat.getServer().await();
}
```

#### 编写Controller
有了Web应用程序的最基本的结构，我们的重点就可以放在如何编写Controller上。Spring MVC对Controller没有固定的要求，也不需要实现特定的接口。以UserController为例，编写Controller只需要遵循以下要点：

总是标记@Controller而不是@Component：
```java
@Controller
public class UserController {
    ...
}
```
一个方法对应一个HTTP请求路径，用@GetMapping或@PostMapping表示GET或POST请求：
```java
@PostMapping("/signin")
public ModelAndView doSignin(
        @RequestParam("email") String email,
        @RequestParam("password") String password,
        HttpSession session) {
    ...
}
```
需要接收的HTTP参数以@RequestParam()标注，可以设置默认值。如果方法参数需要传入HttpServletRequest、HttpServletResponse或者HttpSession，直接添加这个类型的参数即可，Spring MVC会自动按类型传入。

返回的ModelAndView通常包含View的路径和一个Map作为Model，但也可以没有Model，例如：

return new ModelAndView("signin.html"); // 仅View，没有Model
返回重定向时既可以写new ModelAndView("redirect:/signin")，也可以直接返回String：
```java
public String index() {
    if (...) {
        return "redirect:/signin";
    } else {
        return "redirect:/profile";
    }
}
```
如果在方法内部直接操作HttpServletResponse发送响应，返回null表示无需进一步处理：
```java
public ModelAndView download(HttpServletResponse response) {
    byte[] data = ...
    response.setContentType("application/octet-stream");
    OutputStream output = response.getOutputStream();
    output.write(data);
    output.flush();
    return null;
}
```
对URL进行分组，每组对应一个Controller是一种很好的组织形式，并可以在Controller的class定义出添加URL前缀，例如：
```java
@Controller
@RequestMapping("/user")
public class UserController {
    // 注意实际URL映射是/user/profile
    @GetMapping("/profile")
    public ModelAndView profile() {
        ...
    }

    // 注意实际URL映射是/user/changePassword
    @GetMapping("/changePassword")
    public ModelAndView changePassword() {
        ...
    }
}
```
实际方法的URL映射总是前缀+路径，这种形式还可以有效避免不小心导致的重复的URL映射。

可见，Spring MVC允许我们编写既简单又灵活的Controller实现。


### 使用REST
使用Spring MVC开发Web应用程序的主要工作就是编写Controller逻辑。在Web应用中，除了需要使用MVC给用户显示页面外，还有一类API接口，我们称之为REST，通常输入输出都是JSON，便于第三方调用或者使用页面JavaScript与之交互。

直接在Controller中处理JSON是可以的，因为Spring MVC的@GetMapping和@PostMapping都支持指定输入和输出的格式。如果我们想接收JSON，输出JSON，那么可以这样写：
```java
@PostMapping(value = "/rest",
             consumes = "application/json;charset=UTF-8",
             produces = "application/json;charset=UTF-8")
@ResponseBody
public String rest(@RequestBody User user) {
    return "{\"restSupport\":true}";
}
```
对应的Maven工程需要加入Jackson这个依赖：com.fasterxml.jackson.core:jackson-databind:2.11.0

注意到@PostMapping使用consumes声明能接收的类型，使用produces声明输出的类型，并且额外加了@ResponseBody表示返回的String无需额外处理，直接作为输出内容写入HttpServletResponse。输入的JSON则根据注解@RequestBody直接被Spring反序列化为User这个JavaBean。

使用curl命令测试一下：
```bash
$ curl -v -H "Content-Type: application/json" -d '{"email":"bob@example.com"}' http://localhost:8080/rest      
> POST /rest HTTP/1.1
> Host: localhost:8080
> User-Agent: curl/7.64.1
> Accept: */*
> Content-Type: application/json
> Content-Length: 27
> 
< HTTP/1.1 200 
< Content-Type: application/json;charset=utf-8
< Content-Length: 20
< Date: Sun, 10 May 2020 09:56:01 GMT
< 
{"restSupport":true}
```
输出正是我们写入的字符串。

直接用Spring的Controller配合一大堆注解写REST太麻烦了，因此，Spring还额外提供了一个@RestController注解，使用@RestController替代@Controller后，每个方法自动变成API接口方法。我们还是以实际代码举例，编写ApiController如下：
```java
@RestController
@RequestMapping("/api")
public class ApiController {
    @Autowired
    UserService userService;

    @GetMapping("/users")
    public List<User> users() {
        return userService.getUsers();
    }

    @GetMapping("/users/{id}")
    public User user(@PathVariable("id") long id) {
        return userService.getUserById(id);
    }

    @PostMapping("/signin")
    public Map<String, Object> signin(@RequestBody SignInRequest signinRequest) {
        try {
            User user = userService.signin(signinRequest.email, signinRequest.password);
            return Map.of("user", user);
        } catch (Exception e) {
            return Map.of("error", "SIGNIN_FAILED", "message", e.getMessage());
        }
    }

    public static class SignInRequest {
        public String email;
        public String password;
    }
}
```
编写REST接口只需要定义@RestController，然后，每个方法都是一个API接口，输入和输出只要能被Jackson序列化或反序列化为JSON就没有问题。我们用浏览器测试GET请求，可直接显示JSON响应：

user-api

要测试POST请求，可以用curl命令：
```bash
$ curl -v -H "Content-Type: application/json" -d '{"email":"bob@example.com","password":"bob123"}' http://localhost:8080/api/signin
> POST /api/signin HTTP/1.1
> Host: localhost:8080
> User-Agent: curl/7.64.1
> Accept: */*
> Content-Type: application/json
> Content-Length: 47
> 
< HTTP/1.1 200 
< Content-Type: application/json
< Transfer-Encoding: chunked
< Date: Sun, 10 May 2020 08:14:13 GMT
< 
{"user":{"id":1,"email":"bob@example.com","password":"bob123","name":"Bob",...
```
注意观察上述JSON的输出，User能被正确地序列化为JSON，但暴露了password属性，这是我们不期望的。要避免输出password属性，可以把User复制到另一个UserBean对象，该对象只持有必要的属性，但这样做比较繁琐。另一种简单的方法是直接在User的password属性定义处加上@JsonIgnore表示完全忽略该属性：
```java
public class User {
    ...

    @JsonIgnore
    public String getPassword() {
        return password;
    }

    ...
}
```
但是这样一来，如果写一个register(User user)方法，那么该方法的User对象也拿不到注册时用户传入的密码了。如果要允许输入password，但不允许输出password，即在JSON序列化和反序列化时，允许写属性，禁用读属性，可以更精细地控制如下：
```java
public class User {
    ...

    @JsonProperty(access = Access.WRITE_ONLY)
    public String getPassword() {
        return password;
    }

    ...
}
```
同样的，可以使用@JsonProperty(access = Access.READ_ONLY)允许输出，不允许输入。


### 集成Filter
在Spring MVC中，DispatcherServlet只需要固定配置到web.xml中，剩下的工作主要是专注于编写Controller。

但是，在Servlet规范中，我们还可以使用Filter。如果要在Spring MVC中使用Filter，应该怎么做？

有的童鞋在上一节的Web应用中可能发现了，如果注册时输入中文会导致乱码，因为Servlet默认按非UTF-8编码读取参数。为了修复这一问题，我们可以简单地使用一个EncodingFilter，在全局范围类给HttpServletRequest和HttpServletResponse强制设置为UTF-8编码。

可以自己编写一个EncodingFilter，也可以直接使用Spring MVC自带的一个CharacterEncodingFilter。配置Filter时，只需在web.xml中声明即可：

<web-app>
    <filter>
        <filter-name>encodingFilter</filter-name>
        <filter-class>org.springframework.web.filter.CharacterEncodingFilter</filter-class>
        <init-param>
            <param-name>encoding</param-name>
            <param-value>UTF-8</param-value>
        </init-param>
        <init-param>
            <param-name>forceEncoding</param-name>
            <param-value>true</param-value>
        </init-param>
    </filter>

    <filter-mapping>
        <filter-name>encodingFilter</filter-name>
        <url-pattern>/*</url-pattern>
    </filter-mapping>
    ...
</web-app>
因为这种Filter和我们业务关系不大，注意到CharacterEncodingFilter其实和Spring的IoC容器没有任何关系，两者均互不知晓对方的存在，因此，配置这种Filter十分简单。

我们再考虑这样一个问题：如果允许用户使用Basic模式进行用户验证，即在HTTP请求中添加头Authorization: Basic email:password，这个需求如何实现？

编写一个AuthFilter是最简单的实现方式：

@Component
public class AuthFilter implements Filter {
    @Autowired
    UserService userService;

    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {
        HttpServletRequest req = (HttpServletRequest) request;
        // 获取Authorization头:
        String authHeader = req.getHeader("Authorization");
        if (authHeader != null && authHeader.startsWith("Basic ")) {
            // 从Header中提取email和password:
            String email = prefixFrom(authHeader);
            String password = suffixFrom(authHeader);
            // 登录:
            User user = userService.signin(email, password);
            // 放入Session:
            req.getSession().setAttribute(UserController.KEY_USER, user);
        }
        // 继续处理请求:
        chain.doFilter(request, response);
    }
}
现在问题来了：在Spring中创建的这个AuthFilter是一个普通Bean，Servlet容器并不知道，所以它不会起作用。

如果我们直接在web.xml中声明这个AuthFilter，注意到AuthFilter的实例将由Servlet容器而不是Spring容器初始化，因此，@Autowire根本不生效，用于登录的UserService成员变量永远是null。

所以，得通过一种方式，让Servlet容器实例化的Filter，间接引用Spring容器实例化的AuthFilter。Spring MVC提供了一个DelegatingFilterProxy，专门来干这个事情：

<web-app>
    <filter>
        <filter-name>authFilter</filter-name>
        <filter-class>org.springframework.web.filter.DelegatingFilterProxy</filter-class>
    </filter>

    <filter-mapping>
        <filter-name>authFilter</filter-name>
        <url-pattern>/*</url-pattern>
    </filter-mapping>
    ...
</web-app>
我们来看实现原理：

Servlet容器从web.xml中读取配置，实例化DelegatingFilterProxy，注意命名是authFilter；
Spring容器通过扫描@Component实例化AuthFilter。
当DelegatingFilterProxy生效后，它会自动查找注册在ServletContext上的Spring容器，再试图从容器中查找名为authFilter的Bean，也就是我们用@Component声明的AuthFilter。

DelegatingFilterProxy将请求代理给AuthFilter，核心代码如下：

public class DelegatingFilterProxy implements Filter {
    private Filter delegate;
    public void doFilter(...) throws ... {
        if (delegate == null) {
            delegate = findBeanFromSpringContainer();
        }
        delegate.doFilter(req, resp, chain);
    }
}
这就是一个代理模式的简单应用。我们画个图表示它们之间的引用关系如下：

┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐ ┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
  ┌─────────────────────┐        ┌───────────┐   │
│ │DelegatingFilterProxy│─│─│─ ─>│AuthFilter │
  └─────────────────────┘        └───────────┘   │
│ ┌─────────────────────┐ │ │    ┌───────────┐
  │  DispatcherServlet  │─ ─ ─ ─>│Controllers│   │
│ └─────────────────────┘ │ │    └───────────┘
                                                 │
│    Servlet Container    │ │  Spring Container
 ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘
如果在web.xml中配置的Filter名字和Spring容器的Bean的名字不一致，那么需要指定Bean的名字：

<filter>
    <filter-name>basicAuthFilter</filter-name>
    <filter-class>org.springframework.web.filter.DelegatingFilterProxy</filter-class>
    <!-- 指定Bean的名字 -->
    <init-param>
        <param-name>targetBeanName</param-name>
        <param-value>authFilter</param-value>
    </init-param>
</filter>
实际应用时，尽量保持名字一致，以减少不必要的配置。

要使用Basic模式的用户认证，我们可以使用curl命令测试。例如，用户登录名是tom@example.com，口令是tomcat，那么先构造一个使用URL编码的用户名:口令的字符串：

tom%40example.com:tomcat
对其进行Base64编码，最终构造出的Header如下：

Authorization: Basic dG9tJTQwZXhhbXBsZS5jb206dG9tY2F0
使用如下的curl命令并获得响应如下：

$ curl -v -H 'Authorization: Basic dG9tJTQwZXhhbXBsZS5jb206dG9tY2F0' http://localhost:8080/profile
> GET /profile HTTP/1.1
> Host: localhost:8080
> User-Agent: curl/7.64.1
> Accept: */*
> Authorization: Basic dG9tJTQwZXhhbXBsZS5jb206dG9tY2F0
> 
< HTTP/1.1 200 
< Set-Cookie: JSESSIONID=CE0F4BFC394816F717443397D4FEABBE; Path=/; HttpOnly
< Content-Type: text/html;charset=UTF-8
< Content-Language: en-CN
< Transfer-Encoding: chunked
< Date: Wed, 29 Apr 2020 00:15:50 GMT
< 
<!doctype html>
...HTML输出...
上述响应说明AuthFilter已生效。

 注意：Basic认证模式并不安全，本节只用来作为使用Filter的示例。


### 使用Interceptor
在Web程序中，注意到使用Filter的时候，Filter由Servlet容器管理，它在Spring MVC的Web应用程序中作用范围如下：

         │   ▲
         ▼   │
       ┌───────┐
       │Filter1│
       └───────┘
         │   ▲
         ▼   │
       ┌───────┐
┌ ─ ─ ─│Filter2│─ ─ ─ ─ ─ ─ ─ ─ ┐
       └───────┘
│        │   ▲                  │
         ▼   │
│ ┌─────────────────┐           │
  │DispatcherServlet│<───┐
│ └─────────────────┘    │      │
   │              ┌────────────┐
│  │              │ModelAndView││
   │              └────────────┘
│  │                     ▲      │
   │    ┌───────────┐    │
│  ├───>│Controller1│────┤      │
   │    └───────────┘    │
│  │                     │      │
   │    ┌───────────┐    │
│  └───>│Controller2│────┘      │
        └───────────┘
└ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘
上图虚线框就是Filter2的拦截范围，Filter组件实际上并不知道后续内部处理是通过Spring MVC提供的DispatcherServlet还是其他Servlet组件，因为Filter是Servlet规范定义的标准组件，它可以应用在任何基于Servlet的程序中。

如果只基于Spring MVC开发应用程序，还可以使用Spring MVC提供的一种功能类似Filter的拦截器：Interceptor。和Filter相比，Interceptor拦截范围不是后续整个处理流程，而是仅针对Controller拦截：

       │   ▲
       ▼   │
     ┌───────┐
     │Filter1│
     └───────┘
       │   ▲
       ▼   │
     ┌───────┐
     │Filter2│
     └───────┘
       │   ▲
       ▼   │
┌─────────────────┐
│DispatcherServlet│<───┐
└─────────────────┘    │
 │              ┌────────────┐
 │              │ModelAndView│
 │              └────────────┘
 │ ┌ ─ ─ ─ ─ ─ ─ ─ ─ ┐ ▲
 │    ┌───────────┐    │
 ├─┼─>│Controller1│──┼─┤
 │    └───────────┘    │
 │ │                 │ │
 │    ┌───────────┐    │
 └─┼─>│Controller2│──┼─┘
      └───────────┘
   └ ─ ─ ─ ─ ─ ─ ─ ─ ┘
上图虚线框就是Interceptor的拦截范围，注意到Controller的处理方法一般都类似这样：

@Controller
public class Controller1 {
    @GetMapping("/path/to/hello")
    ModelAndView hello() {
        ...
    }
}
所以，Interceptor的拦截范围其实就是Controller方法，它实际上就相当于基于AOP的方法拦截。因为Interceptor只拦截Controller方法，所以要注意，返回ModelAndView后，后续对View的渲染就脱离了Interceptor的拦截范围。

使用Interceptor的好处是Interceptor本身是Spring管理的Bean，因此注入任意Bean都非常简单。此外，可以应用多个Interceptor，并通过简单的@Order指定顺序。我们先写一个LoggerInterceptor：

@Order(1)
@Component
public class LoggerInterceptor implements HandlerInterceptor {

    final Logger logger = LoggerFactory.getLogger(getClass());

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        logger.info("preHandle {}...", request.getRequestURI());
        if (request.getParameter("debug") != null) {
            PrintWriter pw = response.getWriter();
            pw.write("<p>DEBUG MODE</p>");
            pw.flush();
            return false;
        }
        return true;
    }

    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {
        logger.info("postHandle {}.", request.getRequestURI());
        if (modelAndView != null) {
            modelAndView.addObject("__time__", LocalDateTime.now());
        }
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
        logger.info("afterCompletion {}: exception = {}", request.getRequestURI(), ex);
    }
}
一个Interceptor必须实现HandlerInterceptor接口，可以选择实现preHandle()、postHandle()和afterCompletion()方法。preHandle()是Controller方法调用前执行，postHandle()是Controller方法正常返回后执行，而afterCompletion()无论Controller方法是否抛异常都会执行，参数ex就是Controller方法抛出的异常（未抛出异常是null）。

在preHandle()中，也可以直接处理响应，然后返回false表示无需调用Controller方法继续处理了，通常在认证或者安全检查失败时直接返回错误响应。在postHandle()中，因为捕获了Controller方法返回的ModelAndView，所以可以继续往ModelAndView里添加一些通用数据，很多页面需要的全局数据如Copyright信息等都可以放到这里，无需在每个Controller方法中重复添加。

我们再继续添加一个AuthInterceptor，用于替代上一节使用AuthFilter进行Basic认证的功能：

@Order(2)
@Component
public class AuthInterceptor implements HandlerInterceptor {

    final Logger logger = LoggerFactory.getLogger(getClass());

    @Autowired
    UserService userService;

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler)
            throws Exception {
        logger.info("pre authenticate {}...", request.getRequestURI());
        try {
            authenticateByHeader(request);
        } catch (RuntimeException e) {
            logger.warn("login by authorization header failed.", e);
        }
        return true;
    }

    private void authenticateByHeader(HttpServletRequest req) {
        String authHeader = req.getHeader("Authorization");
        if (authHeader != null && authHeader.startsWith("Basic ")) {
            logger.info("try authenticate by authorization header...");
            String up = new String(Base64.getDecoder().decode(authHeader.substring(6)), StandardCharsets.UTF_8);
            int pos = up.indexOf(':');
            if (pos > 0) {
                String email = URLDecoder.decode(up.substring(0, pos), StandardCharsets.UTF_8);
                String password = URLDecoder.decode(up.substring(pos + 1), StandardCharsets.UTF_8);
                User user = userService.signin(email, password);
                req.getSession().setAttribute(UserController.KEY_USER, user);
                logger.info("user {} login by authorization header ok.", email);
            }
        }
    }
}
这个AuthInterceptor是由Spring容器直接管理的，因此注入UserService非常方便。

最后，要让拦截器生效，我们在WebMvcConfigurer中注册所有的Interceptor：

@Bean
WebMvcConfigurer createWebMvcConfigurer(@Autowired HandlerInterceptor[] interceptors) {
    return new WebMvcConfigurer() {
        public void addInterceptors(InterceptorRegistry registry) {
            for (var interceptor : interceptors) {
                registry.addInterceptor(interceptor);
            }
        }
        ...
    };
}
 如果拦截器没有生效，请检查是否忘了在WebMvcConfigurer中注册。
处理异常
在Controller中，Spring MVC还允许定义基于@ExceptionHandler注解的异常处理方法。我们来看具体的示例代码：

@Controller
public class UserController {
    @ExceptionHandler(RuntimeException.class)
    public ModelAndView handleUnknowException(Exception ex) {
        return new ModelAndView("500.html", Map.of("error", ex.getClass().getSimpleName(), "message", ex.getMessage()));
    }
    ...
}
异常处理方法没有固定的方法签名，可以传入Exception、HttpServletRequest等，返回值可以是void，也可以是ModelAndView，上述代码通过@ExceptionHandler(RuntimeException.class)表示当发生RuntimeException的时候，就自动调用此方法处理。

注意到我们返回了一个新的ModelAndView，这样在应用程序内部如果发生了预料之外的异常，可以给用户显示一个出错页面，而不是简单的500 Internal Server Error或404 Not Found。例如B站的错误页：

500

可以编写多个错误处理方法，每个方法针对特定的异常。例如，处理LoginException使得页面可以自动跳转到登录页。

使用ExceptionHandler时，要注意它仅作用于当前的Controller，即ControllerA中定义的一个ExceptionHandler方法对ControllerB不起作用。如果我们有很多Controller，每个Controller都需要处理一些通用的异常，例如LoginException，思考一下应该怎么避免重复代码？


### 处理CORS
在开发REST应用时，很多时候，是通过页面的JavaScript和后端的REST API交互。

在JavaScript与REST交互的时候，有很多安全限制。默认情况下，浏览器按同源策略放行JavaScript调用API，即：

如果A站在域名a.com页面的JavaScript调用A站自己的API时，没有问题；

如果A站在域名a.com页面的JavaScript调用B站b.com的API时，将被浏览器拒绝访问，因为不满足同源策略。

同源要求域名要完全相同（a.com和www.a.com不同），协议要相同（http和https不同），端口要相同 。

那么，在域名a.com页面的JavaScript要调用B站b.com的API时，还有没有办法？

办法是有的，那就是CORS，全称Cross-Origin Resource Sharing，是HTML5规范定义的如何跨域访问资源。如果A站的JavaScript访问B站API的时候，B站能够返回响应头Access-Control-Allow-Origin: http://a.com，那么，浏览器就允许A站的JavaScript访问B站的API。

注意到跨域访问能否成功，取决于B站是否愿意给A站返回一个正确的Access-Control-Allow-Origin响应头，所以决定权永远在提供API的服务方手中。

关于CORS的详细信息可以参考MDN文档，这里不再详述。

使用Spring的@RestController开发REST应用时，同样会面对跨域问题。如果我们允许指定的网站通过页面JavaScript访问这些REST API，就必须正确地设置CORS。

有好几种方法设置CORS，我们来一一介绍。

使用@CrossOrigin
第一种方法是使用@CrossOrigin注解，可以在@RestController的class级别或方法级别定义一个@CrossOrigin，例如：

@CrossOrigin(origins = "http://local.liaoxuefeng.com:8080")
@RestController
@RequestMapping("/api")
public class ApiController {
    ...
}
上述定义在ApiController处的@CrossOrigin指定了只允许来自local.liaoxuefeng.com跨域访问，允许多个域访问需要写成数组形式，例如origins = {"http://a.com", "https://www.b.com"})。如果要允许任何域访问，写成origins = "*"即可。

如果有多个REST Controller都需要使用CORS，那么，每个Controller都必须标注@CrossOrigin注解。

使用CorsRegistry
第二种方法是在WebMvcConfigurer中定义一个全局CORS配置，下面是一个示例：

@Bean
WebMvcConfigurer createWebMvcConfigurer() {
    return new WebMvcConfigurer() {
        @Override
        public void addCorsMappings(CorsRegistry registry) {
            registry.addMapping("/api/**")
                    .allowedOrigins("http://local.liaoxuefeng.com:8080")
                    .allowedMethods("GET", "POST")
                    .maxAge(3600);
            // 可以继续添加其他URL规则:
            // registry.addMapping("/rest/v2/**")...
        }
    };
}
这种方式可以创建一个全局CORS配置，如果仔细地设计URL结构，那么可以一目了然地看到各个URL的CORS规则，推荐使用这种方式配置CORS。

使用CorsFilter
第三种方法是使用Spring提供的CorsFilter，我们在集成Filter中详细介绍了将Spring容器内置的Bean暴露为Servlet容器的Filter的方法，由于这种配置方式需要修改web.xml，也比较繁琐，所以推荐使用第二种方式。

测试
当我们配置好CORS后，可以在浏览器中测试一下规则是否生效。

我们先用http://localhost:8080在Chrome浏览器中打开首页，然后打开Chrome的开发者工具，切换到Console，输入一个JavaScript语句来跨域访问API：

$.getJSON( "http://local.liaoxuefeng.com:8080/api/users", (data) => console.log(JSON.stringify(data)));
上述源站的域是http://localhost:8080，跨域访问的是http://local.liaoxuefeng.com:8080，因为配置的CORS不允许localhost访问，所以不出意外地得到一个错误：

cors-deny

浏览题打印了错误原因就是been blocked by CORS policy。

我们再用http://local.liaoxuefeng.com:8080在Chrome浏览器中打开首页，在Console中执行JavaScript访问localhost：

$.getJSON( "http://localhost:8080/api/users", (data) => console.log(JSON.stringify(data)));
因为CORS规则允许来自http://local.liaoxuefeng.com:8080的访问，因此访问成功，打印出API的返回值：

cors-ok


### 国际化

### 异步处理

### WebSocket

## 集成第三方组件

### JavaMail

### JMS

### Scheduler

### 集成JMX
在Spring中，可以方便地集成JMX。

那么第一个问题来了：什么是JMX？

JMX是Java Management Extensions，它是一个Java平台的管理和监控接口。为什么要搞JMX呢？因为在所有的应用程序中，对运行中的程序进行监控都是非常重要的，Java应用程序也不例外。我们肯定希望知道Java应用程序当前的状态，例如，占用了多少内存，分配了多少内存，当前有多少活动线程，有多少休眠线程等等。如何获取这些信息呢？

为了标准化管理和监控，Java平台使用JMX作为管理和监控的标准接口，任何程序，只要按JMX规范访问这个接口，就可以获取所有管理与监控信息。

实际上，常用的运维监控如Zabbix、Nagios等工具对JVM本身的监控都是通过JMX获取的信息。

因为JMX是一个标准接口，不但可以用于管理JVM，还可以管理应用程序自身。下图是JMX的架构：
```
    ┌─────────┐  ┌─────────┐
    │jconsole │  │   Web   │
    └─────────┘  └─────────┘
         │            │
┌ ─ ─ ─ ─│─ ─ ─ ─ ─ ─ ┼ ─ ─ ─ ─
 JVM     ▼            ▼        │
│   ┌─────────┐  ┌─────────┐
  ┌─┤Connector├──┤ Adaptor ├─┐ │
│ │ └─────────┘  └─────────┘ │
  │       MBeanServer        │ │
│ │ ┌──────┐┌──────┐┌──────┐ │
  └─┤MBean1├┤MBean2├┤MBean3├─┘ │
│   └──────┘└──────┘└──────┘
 ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘
```
JMX把所有被管理的资源都称为MBean（Managed Bean），这些MBean全部由MBeanServer管理，如果要访问MBean，可以通过MBeanServer对外提供的访问接口，例如通过RMI或HTTP访问。

注意到使用JMX不需要安装任何额外组件，也不需要第三方库，因为MBeanServer已经内置在JavaSE标准库中了。JavaSE还提供了一个jconsole程序，用于通过RMI连接到MBeanServer，这样就可以管理整个Java进程。

除了JVM会把自身的各种资源以MBean注册到JMX中，我们自己的配置、监控信息也可以作为MBean注册到JMX，这样，管理程序就可以直接控制我们暴露的MBean。因此，应用程序使用JMX，只需要两步：

编写MBean提供管理接口和监控数据；
注册MBean。
在Spring应用程序中，使用JMX只需要一步：

编写MBean提供管理接口和监控数据。
第二步注册的过程由Spring自动完成。我们以实际工程为例，首先在AppConfig中加上@EnableMBeanExport注解，告诉Spring自动注册MBean：

@Configuration
@ComponentScan
@EnableWebMvc
@EnableMBeanExport // 自动注册MBean
@EnableTransactionManagement
@PropertySource({ "classpath:/jdbc.properties" })
public class AppConfig {
    ...
}
剩下的全部工作就是编写MBean。我们以实际问题为例，假设我们希望给应用程序添加一个IP黑名单功能，凡是在黑名单中的IP禁止访问，传统的做法是定义一个配置文件，启动的时候读取：

 blacklist.txt
1.2.3.4
5.6.7.8
2.2.3.4
...
如果要修改黑名单怎么办？修改配置文件，然后重启应用程序。

但是每次都重启应用程序实在是太麻烦了，能不能不重启应用程序？可以自己写一个定时读取配置文件的功能，检测到文件改动时自动重新读取。

上述需求本质上是在应用程序运行期间对参数、配置等进行热更新并要求尽快生效。如果以JMX的方式实现，我们不必自己编写自动重新读取等任何代码，只需要提供一个符合JMX标准的MBean来存储配置即可。

还是以IP黑名单为例，JMX的MBean通常以MBean结尾，因此我们遵循标准命名规范，首先编写一个BlacklistMBean：

public class BlacklistMBean {
    private Set<String> ips = new HashSet<>();

    public String[] getBlacklist() {
        return ips.toArray(String[]::new);
    }

    public void addBlacklist(String ip) {
        ips.add(ip);
    }

    public void removeBlacklist(String ip) {
        ips.remove(ip);
    }

    public boolean shouldBlock(String ip) {
        return ips.contains(ip);
    }
}
这个MBean没什么特殊的，它的逻辑和普通Java类没有任何区别。

下一步，我们要使用JMX的客户端来实时热更新这个MBean，所以要给它加上一些注解，让Spring能根据注解自动把相关方法注册到MBeanServer中：

@Component
@ManagedResource(objectName = "sample:name=blacklist", description = "Blacklist of IP addresses")
public class BlacklistMBean {
    private Set<String> ips = new HashSet<>();

    @ManagedAttribute(description = "Get IP addresses in blacklist")
    public String[] getBlacklist() {
        return ips.toArray(String[]::new);
    }

    @ManagedOperation
    @ManagedOperationParameter(name = "ip", description = "Target IP address that will be added to blacklist")
    public void addBlacklist(String ip) {
        ips.add(ip);
    }

    @ManagedOperation
    @ManagedOperationParameter(name = "ip", description = "Target IP address that will be removed from blacklist")
    public void removeBlacklist(String ip) {
        ips.remove(ip);
    }

    public boolean shouldBlock(String ip) {
        return ips.contains(ip);
    }
}
观察上述代码，BlacklistMBean首先是一个标准的Spring管理的Bean，其次，添加了@ManagedResource表示这是一个MBean，将要被注册到JMX。objectName指定了这个MBean的名字，通常以company:name=Xxx来分类MBean。

对于属性，使用@ManagedAttribute注解标注。上述MBean只有get属性，没有set属性，说明这是一个只读属性。

对于操作，使用@ManagedOperation注解标准。上述MBean定义了两个操作：addBlacklist()和removeBlacklist()，其他方法如shouldBlock()不会被暴露给JMX。

使用MBean和普通Bean是完全一样的。例如，我们在BlacklistInterceptor对IP进行黑名单拦截：

@Order(1)
@Component
public class BlacklistInterceptor implements HandlerInterceptor {
    final Logger logger = LoggerFactory.getLogger(getClass());

    @Autowired
    BlacklistMBean blacklistMBean;

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler)
            throws Exception {
        String ip = request.getRemoteAddr();
        logger.info("check ip address {}...", ip);
        // 是否在黑名单中:
        if (blacklistMBean.shouldBlock(ip)) {
            logger.warn("will block ip {} for it is in blacklist.", ip);
            // 发送403错误响应:
            response.sendError(403);
            return false;
        }
        return true;
    }
}
下一步就是正常启动Web应用程序，不要关闭它，我们打开另一个命令行窗口，输入jconsole启动JavaSE自带的一个JMX客户端程序：

jconsole

通过jconsole连接到一个Java进程最简单的方法是直接在Local Process中找到正在运行的AppConfig，点击Connect即可连接到我们当前正在运行的Web应用，在jconsole中可直接看到内存、CPU等资源的监控。

我们点击MBean，左侧按分类列出所有MBean，可以在java.lang查看内存等信息：

mbean

细心的童鞋可以看到HikariCP连接池也是通过JMX监控的。

在sample中可以看到我们自己的MBean，点击可查看属性blacklist：

mbean-value

点击Operations-addBlacklist，可以填入127.0.0.1并点击addBlacklist按钮，相当于jconsole通过JMX接口，调用了我们自己的BlacklistMBean的addBlacklist()方法，传入的参数就是填入的127.0.0.1：

mbean-invoke-ok

再次查看属性blacklist，可以看到结果已经更新了：

mbean-modified

我们可以在浏览器中测试一下黑名单功能是否已生效：

403

可见，127.0.0.1确实被添加到了黑名单，后台日志打印如下：

2020-06-06 20:22:12 INFO  c.i.l.web.BlacklistInterceptor - check ip address 127.0.0.1...
2020-06-06 20:22:12 WARN  c.i.l.web.BlacklistInterceptor - will block ip 127.0.0.1 for it is in blacklist.
注意：如果使用IPv6，那么需要把0:0:0:0:0:0:0:1这个本机地址加到黑名单。

如果从jconsole中调用removeBlacklist移除127.0.0.1，刷新浏览器可以看到又允许访问了。

使用jconsole直接通过Local Process连接JVM有个限制，就是jconsole和正在运行的JVM必须在同一台机器。如果要远程连接，首先要打开JMX端口。我们在启动AppConfig时，需要传入以下JVM启动参数：

-Dcom.sun.management.jmxremote.port=19999
-Dcom.sun.management.jmxremote.authenticate=false
-Dcom.sun.management.jmxremote.ssl=false
第一个参数表示在19999端口监听JMX连接，第二个和第三个参数表示无需验证，不使用SSL连接，在开发测试阶段比较方便，生产环境必须指定验证方式并启用SSL。详细参数可参考Oracle官方文档。这样jconsole可以用ip:19999的远程方式连接JMX。连接后的操作是完全一样的。

许多JavaEE服务器如JBoss的管理后台都是通过JMX提供管理接口，并由Web方式访问，对用户更加友好。



# Spring Boot

## 